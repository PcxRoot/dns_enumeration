import dns.resolver
import whois
import argparse
import sys
from banner import banner


# Funcion para hacer las consulatas a las bases de datos WHOIS
def bbdd_whois(domains):
    print()
    print('\n  *********************************************************************')
    print('WHOIS DATABASES'.center(65))
    print('  *********************************************************************')

    for d in domains:
        try:
            response = whois.whois(d)       # Almacenamos las respuestas de la consulta
        except Exception as e:              
            texto = f'WHOIS: {d} --> Dominio no encontrado o error'
            anchura_total = 75                                          # En caso de error nos mostrara un panel que lo indique
            print(f'\n    {"*" * anchura_total}')
            print(' ' * 4 + texto.center(anchura_total))
            print(f'    {"*" * anchura_total}')
            continue                                        # Pasamos a el siguiente dominio.
        
        texto = f'WHOIS: {d}'
        anchura_total = 65
        print(f'\n    {"*" * anchura_total}')
        print(' ' * 4 + texto.center(anchura_total))        # En el caso de que no haya problemas, se imprime un banner especificando el dominio al que precede la informacion
        print(f'    {"*" * anchura_total}')
        print(f'{response}')        


# Funcion para hacer las consulats DNS
def info(domains, records):
    if records == '':               # Si el usuario no especifica RR, se usuara el predeterminado ("A")
        record_types = ['A']
    else:
        record_types = [r.strip().upper() for r in records.split(',')]      # Si el usuario especifica registros, se ponen en el formato adecuado


    resolver = dns.resolver.Resolver()          # Creamos el DNS resolver
    for target in domains:
        print(f'\n    {"*" * 65}')
        print(f' ' * 4 + f'Registros del dominio: {target}'.center(65))     # Banner del dominio
        print(f'    {"*" * 65}')
        fallo = False                           # Variable que nos permite ver si el dominio es erroneo. Nos permite que el bucle no siga buscando en un dominio inexistente
        for record_type in record_types:
            if fallo == False:
                try:
                    answers = resolver.resolve(target, record_type)         # Se hace la consulta buscando el RR correspondiente
                except dns.resolver.NoAnswer:
                    continue                                                # En caso de que el dominio exista pero no se encuentre informacion sobre el RR se continua con el bucle
                except dns.resolver.NXDOMAIN:
                    print(f'\n    {"-" * 65}')
                    print(f' ' * 4 + f'El nombre de dominio {target} no existe'.center(65))     # En caso de que no exista el dominio, se muestra un panel indicandolo y no sigue
                    print(f'    {"-" * 65}')                                                    # iterando sobre el mismo dominio
                    fallo = True
                    continue
            

                # Mostramos la informacion de ese registro
                print(f'\n{record_type} registros para {target}')
                for data in answers:                                        # Si se encuentra informacion sobre el RR, se muestra por pantalla
                    print(f'- {data}')
            else:
                continue


# Funcion principal del programa
def main(register, Whois, domain):

    try:
        banner()
    except Exception:
        pass
    
    # Definimos el nombre de dominio
    if not domain:
        print('No se ha especificado ningun dominio. Usa la opcion "-h" para mas informacion.')     # Si no se especifica algun dominio, salta un error
        print('Ejemplo: %s -d "example.com"' % sys.argv[0])
        sys.exit(1)
    target_domains = domain.split(',')              # Divide los dominios en una lista usando las comas

    if register is not None:
        info(target_domains, register)              # Si el usuario a usado la opcion -R, se llama a la funcion info con la lista de los dominios y los RR como parametros
        
    if Whois or register is None:                   
        bbdd_whois(target_domains)                  # Si el usuario especifica la opcion --whois o no usa la opcion -R, se llama a la funcion bbdd_whois con la lista de
                                                    # de los dominios como parametro

# En el caso de que el programa se use directamente desde terminal y no como modulo aparte
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Esta herramienta permite hacer consultas DNS para sacar informacion de los distintos RR y/o de las bases de datos "Whois".Se pueden unir las opciones -R y --whois para obtener informacion tanto de los registros DNS como de las bases de datos Whois. Ej: %s -d "example.com" -R "A,AAAA,MX,CNAME" --whois' % sys.argv[0])
    parser.add_argument('-d', '--domain', type=str,
                        help='[OBLIGATORIO] Especifica los dominios a consultar separados por comas. Ej: %s -d "example.com"' % sys.argv[0])    
    parser.add_argument('-R', '--register', nargs='?', const='', default=None,
                        help='Definir los registros a consultar separados por comas. Si no se especifican registros el predeterminado es "A". Si no se usa esta opcion, se usara la opcion "--whois". Ej: %s -d "example.com" -R "A,AAAA,MX"' % sys.argv[0])
    parser.add_argument('--whois', action='store_true',
                        help='Muestra el resultado de la consulta a las bases de datos "Whois". Ej: %s -d "example.com" -R --whois' % sys.argv[0])
    args = parser.parse_args()

    main(register=args.register,
        Whois = args.whois,
        domain = args.domain)