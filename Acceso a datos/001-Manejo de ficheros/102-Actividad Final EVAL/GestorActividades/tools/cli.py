"""Herramienta CLI mínima para exportar/importar y operar con datos.
"""
import argparse
from services.activity_service import ActivityService
from services.import_export import export_csv, import_csv


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--export', help='Destino CSV', default=None)
    p.add_argument('--import', dest='import_file', help='Importar CSV', default=None)
    args = p.parse_args()
    svc = ActivityService()
    if args.export:
        export_csv(svc.list_all(), args.export)
        print('Exportado a', args.export)
    if args.import_file:
        items = import_csv(args.import_file)
        for it in items:
            try:
                svc.create(it)
            except Exception as e:
                print('Error importar', e)

if __name__ == '__main__':
    main()
