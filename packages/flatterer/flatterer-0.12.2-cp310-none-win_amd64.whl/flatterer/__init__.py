import decimal
import click

import orjson

from .flatterer import iterator_flatten_rs, flatten_rs, setup_logging, setup_ctrlc

LOGGING_SETUP = False


def default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError


def bytes_generator(iterator):
    for item in iterator:
        if isinstance(item, bytes):
            yield item
        if isinstance(item, str):
            yield str.encode()
        if isinstance(item, dict):
            yield orjson.dumps(item, default=default)


def flatten(
    input,
    output_dir,
    csv=True,
    xlsx=False,
    sqlite=False,
    path='',
    main_table_name='main',
    emit_path=[],
    json_lines=False,
    force=False,
    fields='',
    only_fields=False,
    tables='',
    only_tables=False,
    inline_one_to_one=False,
    schema="",
    table_prefix="",
    path_separator="_",
    schema_titles="",
    sqlite_path="",
    preview=0,
    log_error=False,
):
    global LOGGING_SETUP
    if not LOGGING_SETUP:
        setup_logging("warning")
        LOGGING_SETUP = True
    flatten_rs(input, output_dir, csv, xlsx, sqlite,
               path, main_table_name, emit_path, json_lines, force, fields, only_fields, tables, 
               only_tables, inline_one_to_one, schema, table_prefix, path_separator, schema_titles, 
               sqlite_path, preview, log_error)


def iterator_flatten(
    iterator,
    output_dir,
    csv=True,
    xlsx=False,
    sqlite=False,
    main_table_name='main',
    emit_path=[],
    force=False,
    fields='',
    only_fields=False,
    tables='',
    only_tables=False,
    inline_one_to_one=False,
    schema="",
    table_prefix="",
    path_separator="_",
    schema_titles="",
    sqlite_path="",
    preview=0,
    log_error=False
):
    global LOGGING_SETUP
    if not LOGGING_SETUP:
        setup_logging("warning")
        LOGGING_SETUP = True
    iterator_flatten_rs(bytes_generator(iterator), output_dir, csv, xlsx, sqlite,
                        main_table_name, emit_path, force, fields, only_fields, tables,
                        only_tables, inline_one_to_one, schema, table_prefix, path_separator,
                        schema_titles, sqlite_path, preview, log_error)


@click.command()
@click.option('--csv/--nocsv', default=True, help='Output CSV files, default true')
@click.option('--xlsx/--noxlsx', default=False, help='Output XLSX file, default false')
@click.option('--sqlite/--nosqlite', default=False, help='Output sqlite.db file, default false')
@click.option('--main-table-name', '-m', default=None,
              help='Name of main table, defaults to name of the file without the extension')
@click.option('--path', '-p', default='', help='Key name of where json array starts, default top level array')
@click.option('--json-lines', '-j', is_flag=True, default=False,
              help='Is file a jsonlines file, default false')
@click.option('--force', is_flag=True, default=False,
              help='Delete output directory if it exists, then run command, default False')
@click.option('--fields', '-f', default="", help='fields.csv file to use')
@click.option('--only-fields', '-o', is_flag=True, default=False, help='Only output fields in fields.csv file')
@click.option('--tables', '-b', default="", help='tables.csv file to use')
@click.option('--only-tables', '-l', is_flag=True, default=False, help='Only output tables in tables.csv file')
@click.option('--inline-one-to-one', '-i', is_flag=True, default=False,
              help='If array only has single item for all objects treat as one-to-one')
@click.option('--schema', '-s', default="",
              help='JSONSchema file or URL to determine field order')
@click.option('--table-prefix', '-t', default="",
              help='Prefix to add to all table names')
@click.option('--path-separator', '-a', default="_",
              help='Seperator to denote new path within the input JSON. Defaults to `_`')
@click.option('--schema-titles', '-h', default="",
              help='Use titles from JSONSchema in the given way. Options are `full`, `slug`, `underscore_slug`. Default to not using titles')
@click.option('--preview', '-w', default=0,
              help='Only output this `preview` amount of lines in final results')
@click.argument('input_file')
@click.argument('output_directory')
def cli(
    input_file,
    output_directory,
    csv=True,
    xlsx=False,
    sqlite=False,
    path='',
    main_table_name=None,
    json_lines=False,
    force=False,
    fields="",
    only_fields=False,
    tables="",
    only_tables=False,
    inline_one_to_one=False,
    schema="",
    table_prefix="",
    path_separator="_",
    schema_titles="",
    preview=0
):
    global LOGGING_SETUP
    if not LOGGING_SETUP:
        setup_logging("info")
        LOGGING_SETUP = True
        setup_ctrlc()

    if not main_table_name:
        main_table_name = input_file.split('/')[-1].split('.')[0]

    try:
        flatten(input_file,
                output_directory,
                csv=csv,
                xlsx=xlsx,
                sqlite=sqlite,
                path=path,
                main_table_name=main_table_name,
                json_lines=json_lines,
                force=force,
                fields=fields,
                only_fields=only_fields,
                tables=tables,
                only_tables=only_tables,
                inline_one_to_one=inline_one_to_one,
                schema=schema,
                table_prefix=table_prefix,
                path_separator=path_separator,
                schema_titles=schema_titles,
                preview=preview,
                log_error=True)
    except IOError:
        pass
