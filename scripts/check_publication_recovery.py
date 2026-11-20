"""Read-only preflight for an authorized, standalone SQLite backup."""
from __future__ import annotations

import argparse
import sqlite3
from contextlib import closing
from pathlib import Path

from app.group_policy import validate_recovery_rules


def inspect_backup(path: Path) -> dict[str, int]:
    path = path.resolve(strict=True)
    if not path.is_file() or any(Path(str(path) + suffix).exists() for suffix in ('-wal', '-journal')):
        raise ValueError('需要由 SQLite backup 生成的独立数据库副本')
    with closing(sqlite3.connect(f'{path.as_uri()}?mode=ro&immutable=1', uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA query_only=ON')
        if connection.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
            raise ValueError('SQLite 完整性核验失败')
        if connection.execute('PRAGMA foreign_key_check').fetchone():
            raise ValueError('存在失效的数据库关联')
        validate_recovery_rules(connection)
        return {
            name: connection.execute(f'SELECT count(*) FROM {name}').fetchone()[0]
            for name in ('researchers', 'papers', 'researcher_papers', 'scholar_review_rules',
                         'paper_overrides', 'researcher_paper_overrides')
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('backup', type=Path)
    args = parser.parse_args()
    try:
        counts = inspect_backup(args.backup)
    except (OSError, sqlite3.Error, ValueError) as error:
        parser.exit(1, f'预检失败（{type(error).__name__}）：请核对独立备份、数据库结构和已批准排除规则。\n')
    for table, count in counts.items():
        print(f'{table}: {count}')
    print('备份完整性和排除规则预检通过。')


if __name__ == '__main__':
    main()
