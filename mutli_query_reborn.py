import signal
import os
import logging
import multiprocessing
import subprocess
import configparser
import utility.globalvar as gl
import time

# Global variable to keep track of the running processes
processes = []

def read_ini():
    gl._init()
    print("[*]Reading configuration from config.ini...")
    try:
        config = configparser.ConfigParser()
        config.read("./config.ini", encoding='utf-8')
        # read miniapp_dict and query_dir
        miniapp_dict = config.get('Query Paths', 'miniapp_dict')
        query_dir = config.get('Query Paths', 'query_dir')
        dec_dir = config.get('Query Paths', 'dec_dir')
        # (windows only) read Wechat IDE cli path
        ide_cli = config.get('Minitest path', 'ide_cli')
        if miniapp_dict and query_dir and ide_cli:
            print("[*]The configuration has been set.")
            # set configuration to global
            gl.set_value('miniapp_dict', miniapp_dict)
            gl.set_value('query_dir', query_dir)
            gl.set_value('ide_cli', ide_cli)
            gl.set_value("dec_dir", dec_dir)
            return True
        else:
            print("[!]Some values may be empty. Please check your config.ini :/")
            exit(1)
    except:
        print("[!]Missing value of the configuration. Please check your config.ini :/")
        exit(1)

def run_script(script_path, log_file, dir_name):
    # Configure logging
    log_format = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(filename=log_file, level=logging.INFO, format=log_format)

    try:
        # Run the Python script with the specified arguments and log the output
        output = subprocess.check_output(['python', script_path, '-s', dir_name], stderr=subprocess.STDOUT)
        logging.info(output.decode('utf-8', 'ignore'))
    except subprocess.CalledProcessError as e:
        # Log the error message if the script exits abnormally
        logging.error("Python script exited with error. Error message: %s", e.output.decode())

def stop_execution(signum, frame):
    # Terminate all running processes
    for p in processes:
        p.terminate()
    # Wait for all the processes to finish
    for p in processes:
        p.join()
    # Exit the main process
    exit(0)

if __name__ == '__main__':
    start_time = time.time()
    # Define the script path and log directory
    python_script = "./main_reborn.py"
    log_directory = "./log"

    # Create the log directory if it doesn't exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Register the signal handler for stopping execution,ONLY IN LINUX
    signal.signal(signal.SIGINT, stop_execution)

    # Read the configuration from config.ini
    read_ini()

    # Get the list of directories
    miniapp_dict = gl.get_value("miniapp_dict")
    dirs = os.listdir(miniapp_dict)
    if dirs is None:
        print("Nothing in your miniapp_dict. Please check your config file.")
        exit(1)

    # Set the maximum number of concurrent processes
    max_concurrent_processes = 1

    # Create a multiprocessing pool with the maximum number of processes
    pool = multiprocessing.Pool(processes=max_concurrent_processes)

    # Submit tasks to the pool
    for sub_dir in dirs:
        log_file = os.path.join(log_directory, f"log_{sub_dir}.txt")
        pool.apply_async(run_script, args=(python_script, log_file, sub_dir))

    # Close the pool and wait for all tasks to complete
    pool.close()
    pool.join()

    # Calculate and save execution time
    end_time = time.time()
    execution_time = end_time - start_time

    with open("./multi_time.txt", "w") as file:
        file.write(str(execution_time))
