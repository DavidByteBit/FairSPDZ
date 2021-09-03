PRE_PROCESS_FUNC = {'img': 'pre_process_images', 'tab': 'pre_process_tab', 'aud': 'pre_process_audio',
                    'other': 'pre_process_other'}

SAMPLE_MPC_PUBLIC_FILE_INFER = {'img': 'imagesClassify', 'tab': 'tabClassify', 'aud': None, 'other': None}

SAMPLE_MPC_PUBLIC_FILE_FAIR = {'img': 'evalFairImages', 'tab': 'evalFairTab', 'aud': None, 'other': None}

SAMPLE_MPC_PROG_NAME_INFER = {'img': 'imagesClassify', 'tab': 'tabClassify', 'aud': None, 'other': None}

SAMPLE_MPC_PROG_NAME_FAIR = {'img': 'evalFairImages', 'tab': 'evalFairTab', 'aud': None, 'other': None}

FILE_PROCESSOR_INFER = {'img': 'process_mpc_output_images_infer', 'tab': 'process_mpc_output_tab',
                        'aud': 'process_mpc_output_aud',
                  'other': 'process_mpc_output_other'}

FILE_PROCESSOR_FAIR = {'img': 'process_mpc_output_images_fair', 'tab': 'process_mpc_output_tab',
                       'aud': 'process_mpc_output_aud',
                        'other': 'process_mpc_output_other'}

SAMPLE_MPC_PROG_NAME = {'img': 'evalFairImagesClassify', 'tab': 'evalFairTabClassify',
                        'aud': None, 'other': None}

NUM_MPC_VMS = 1

MPC_HOSTS = ['172.10.0.2','172.10.0.3']

MPC_PROTOCOL = {1:'Scripts/ring.sh', 2:'./semi2k-party.x -p 0', 3: './replicated-ring-party.x -p 0'}

MPC_PORT = 2000


