
"""
TO DO:

1) Entrar a linkedin  ✔️✔️
2) En el buscador poner la palabra por parametro de busqueda ✔️✔️
3) Filtrar para buscar solo compañias ✔️✔️
4) Filtrar por pais pasado por parametro (poner opciones por defecto)  ✔️✔️
5) Filtrar por industrias de interes por parametro (poner opciones por defecto) ✔️✔️
6) Entrar a una empresa en los resultados de busqueda ✔️✔️
7) Entrar a "pesonas" ✔️✔️
8) Poner las palabras clave ✔️✔️
9) Verificar en los resultados, las personas que cumplen con el 
                                nombre de la compania y la posicion ✔️✔️
8) Entrar en los perfiles de las personas que cumplen con eso y 
                                mandar una solicitus de conexion.  ✔️✔️
9) Guardar a la persona en la base de datos 
        {(Nombre, Empresa, Palabras clave, linkedin link, 
                    solicitud enviada<bool>, amigo<bool>)}   ✔️✔️
10) Exportar la base de datos  ✔️✔️
11) Exportar las opciones o imputs del programa  ✔️✔️
12) Verificar estado de contactos segun base de datos externa
13) Mandar solicitud de conextion a contactos segun base de datos externa.
14) Exportar la nueva base de datos con los contactos actualizados.

TO DO
OJO: bot.filter_industry(filter_num=4,custom_filters=default_dict['custom_filters_industry']
                            filter num hay q cambiarlo!!! 

'keywords':['CEO', 'chief executive officer', 'COO', 'chief operating officer',
                                     'Owner', 'Founder', 'Co-Founder', 'President', 'Director'],


"""
from botLib.main import Bot
import time
import pandas as pd
import getpass
import datetime
import os
import traceback

default_dict = {'email':['NULL'], 'password':['NULL'], 'search_value':['Staffing'], 
                        'filter_num_location':[6], 'custom_filters_location':['Colombia'], 
                        'filter_num_industry':[6], 'custom_filters_industry':['Software'],
                         'keywords':['Founder'],
                        'campaignnumber':['NULL'], 'campaigndate':[datetime.date.today().strftime("%Y/%m/%d")]}

lang = input('\nChose a language: [EN]glish/[ES]pañol: ').lower()

if lang == 'es':

    print('Bienvenido. \n')
    contact_list = input('Desea verificar una lista de contactos existentes? [S]í/[N]o: ').lower()
    if contact_list == 's':
        path = input('Escribe la ruta completa del archivo: ')
        print('Por favor, proporcione correo electrónico y contraseña (por seguridad, nada se almacenará):\n')
        email = input('Correo: ').lower()
        password = getpass.getpass()
    else:
        instructions = input('¿Tiene instrucciones preestablecidas para cargar? [S]í/[N]o: ').lower()
        if instructions == 's':
            path = input('Escribe la ruta completa del archivo: ')
            loaded_dict = pd.read_csv(path)
            loaded_dict = loaded_dict.to_dict('list')
            default_dict['custom_filters_location'] = ','.join(loaded_dict['custom_filters_location']).split(',')
            default_dict['custom_filters_industry'] = ','.join(loaded_dict['custom_filters_industry']).split(',')
            try:
                default_dict['email'] = loaded_dict['email']
                default_dict['password'] = loaded_dict['password']
            except:
                print('Por favor, proporcione correo electrónico y contraseña (por seguridad, nada se almacenará):\n')
                email = input('Correo: ').lower()
                password = getpass.getpass()
                default_dict['email'] = [email]
                default_dict['password'] = [password]

            campaign = input("Proporcione el número de la campaña a ser creada: ")
            default_dict['campaignnumber'] = [int(campaign)]
            path = os.getcwd()
            save_input = None
        elif instructions == 'n':
            print('Por favor, proporcione correo electrónico y contraseña (por seguridad, nada se almacenará):\n')
            email = input('Correo: ').lower()
            password = getpass.getpass()
            campaign = input("Proporcione el número de la campaña a ser creada: ")
            search_value = input('Palabra clave para las empresas que está buscando: ')
            filter_location = input('Filtrar por país. (Si hay más de uno, sepárelos por coma): ').split(",")
            print(filter_location)
            print(type(filter_location))
            filter_industry = input('Filtrar por industria. (Si hay más de una, sepárelos por coma): ').split(",")
            save_input = input('¿Quiere guardar las siguientes instrucciones en un archivo para uso futuro? (Tenga la seguridad de que todo se almacenará solo en el archivo de salida y podrá borrarlos manualmente si lo desea.) \n [S]í/[N]o): ').lower()
            if save_input == 's':
                path = input('Quiere guardarlo en alguna ruta en especifico? (Por defecto se guarda en la ruta actual) [N]ueva/[D]efecto: ').lower()
                if path == 'd':
                    path = os.getcwd()

            default_dict['email'] = [email]
            default_dict['password'] = [password]
            default_dict['campaignnumber'] = [int(campaign)]
            default_dict['search_value'] = [search_value]
            default_dict['custom_filters_location'] = filter_location
            default_dict['custom_filters_industry'] = filter_industry
        
else:

    print('Welcome. \n')
    contact_list = input('Do you want to verify an existing list of contacs? [Y]es/[N]o: ').lower()
    if contact_list == 'y':
        path = input('Write the complete route of the file: ')
        print('Please provide email and password (For security, nothing will be stored):\n')
        email = input('Email: ').lower()
        password = getpass.getpass()
    else:
        instructions = input('Do you have preset directions to load? [Y]es/[N]o: ').lower()
        if instructions == 'y':
            path = input('Write the complete route of the file: ')
            loaded_dict = pd.read_csv(path)
            loaded_dict = loaded_dict.to_dict('list')
            default_dict['custom_filters_location'] = ','.join(loaded_dict['custom_filters_location']).split(',')
            default_dict['custom_filters_industry'] = ','.join(loaded_dict['custom_filters_industry']).split(',')
            try:
                default_dict['email'] = loaded_dict['email']
                default_dict['password'] = loaded_dict['password']
            except:
                print('Please provide email and password (For security, nothing will be stored):\n')
                email = input('Email: ').lower()
                password = getpass.getpass()
                default_dict['email'] = [email]
                default_dict['password'] = [password]

            campaign = input("Provide number to the campaign that is about to be created: ")
            default_dict['campaignnumber'] = [int(campaign)]
            path = os.getcwd()
            save_input = None
                
        elif instructions == 'n':
            print('Please provide email and password (For security, nothing will be stored):\n ')
            email = input('Email: ').lower()
            password = getpass.getpass()
            campaign = input("Provide number to the campaign that is about to be created: ")
            search_value = input('Keyword for compaies you are looking for: ')
            filter_location = input('Filter by country. (IF more than one, separate them by comma): ').split(",")
            filter_industry = input('Filter by industry. (IF more than one, separate them by comma): ').split(",")
            save_input = input('Do you want to save the following directions in a file for future use? (Rest asured, everything will be stored only on the output file and you can manually errase them if you want) \n [Y]es/[N]o: ').lower()
            if save_input == 'y':
                path = input('By default the file is saved in the current directory. You can provide a new route. [N]ew/[D]efault: ').lower()
                if path == 'd':
                    path = os.getcwd()
            default_dict['email'] = [email]
            default_dict['password'] = [password]
            default_dict['campaignnumber'] = [int(campaign)]
            default_dict['search_value'] = [search_value]
            default_dict['custom_filters_location'] = filter_location
            default_dict['custom_filters_industry'] = filter_industry




with Bot(teardown=False) as bot:
    try:
        
        if contact_list == 'n':
            bot.land_first_page()
            
            bot.login(email=default_dict['email'][0],password=default_dict['password'][0])


            bot.search(search_value=default_dict['search_value'][0])


            bot.filter_companies()
            time.sleep(2)

            bot.filter_location(filter_num=6,custom_filters=default_dict['custom_filters_location'])

            bot.filter_industry(filter_num=6,custom_filters=default_dict['custom_filters_industry'])

            dict_data = bot.cycle_companies(keywords=default_dict['keywords'])
            print(f'Dict data recieved about to print \n.\n.\n.')
            total_registers = len(dict_data['Name'])
            dict_data['Campaign Number'] = default_dict['campaignnumber'] * total_registers
            dict_data['Campaign Date'] = default_dict['campaigndate'] * total_registers

            print(dict_data)
            df_dict_data = pd.DataFrame.from_dict(dict_data) 
            print(f'\n csv file about to created')
            print(df_dict_data)
            #Exporting contact list
            df_dict_data.to_csv(f'{path}/contactsList.csv')
            print(f'\n csv file created')
            #Saving instructions
            if save_input == 's' or save_input == 'y':
                del default_dict['campaigndate']
                del default_dict['campaignnumber']
                default_dict['custom_filters_location'] = [','.join(default_dict['custom_filters_location'])]
                default_dict['custom_filters_industry'] = [','.join(default_dict['custom_filters_industry'])]
                print('about to create df_default_dict')
                path = os.getcwd()
                print(path)
                df_default_dict = pd.DataFrame.from_dict(default_dict)
                print('created df_default_dict')
                #/Users/carlosgutierrez/Documents/WORKSPACE/webScraping/PruebaTecnica/
                
                df_default_dict.to_csv(f'{path}/customInput.csv')
        elif contact_list == 's' or contact_list == 'y':
            load_df = pd.read_csv(path)
            df = bot.check_contact_list(df=load_df,email=email,password=password)
            df.to_csv(path)
            
    except Exception as e:
        print('error en el run')
        print(traceback.format_exc())
        print(e)
        time.sleep(10000)
    #time.sleep(1000)

