# MiniCAT

MiniCAT stands for **Mini**-program **C**ross Page Request Forgery (CPRF) **A**nalysis **T**ool. It is an automatic static analysis framework designed to detect MiniCPRF, a novel mini-program vulnerability.

MiniCAT is powered by CodeQL. For more details, please refer to our CCS'24 paper. We recommend allocating at least 4 cores and 16 GiB of memory to run the tool efficiently.

## Prerequisites

### Environment

MiniCAT can be used on both Linux and Windows OS. We recommend allocating at least 4 cores and 16 GiB of memory to run the tool efficiently.

As a reference, we implemented MiniCAT on:

- Windows 10 PC, with i7-9750h and 32GB RAM.
- Ubuntu 20.04 Server, with Intel Xeon Gold 6638 and 256GB RAM.

### Dependencies

To run MiniCAT, you need to have:

- [CodeQL CLI](https://github.com/github/codeql)
- Node.js (we used v16.20.0) & npm
- Python 3 (we used 3.8.10)

To initialize our tool, we provide a pre-check script `initialize.sh` (for Linux) and `initialize.bat` (for Windows). These scripts will check for necessary dependencies and automatically install the required npm packages and Python modules. We recommend running the initialization script before using MiniCAT.

### Configuring `config.ini`

To conduct a large-scale measurement, MiniCAT uses a configuration file for settings.

```ini
[Query Paths]
; Directory where the WeChat mini-programs are stored
; miniapp_dict = C:/Users/Administrator/Documents/WeChat Files/Applet
miniapp_dict = E:/MiniCAT/miniapp_dict
; Directory where this script is stored. After querying, res/ etc. directories will be generated here
query_dir = E:/MiniCAT
; Dec_dir, make sure this directory has enough disk storage.
dec_dir = E:/MiniCAT/dec_dir
; Directory to save the results
; res_dir = E:/Minicat_test/res_dir
```

Please replace or modify the file paths of the config items **(USE ABSOLUTE PATHS)**.

### Statement

MiniCAT relies on wxappUnpacker to unpack mini-programs. Due to potential legal implications, we DO NOT provide wxappUnpacker in our repository. Users should copy it to the wxappUnpacker folder (under the root directory of this repository) by themselves or use pre-unpacked mini-programs for analysis.

## Usage & Examples

1. Place the mini-program raw package in the {Wechat Mini-program Appid} folder and copy it to the `miniapp_dict` directory set in `config.ini`.

  ```
  e.g. E:\MiniCAT\miniapp_dict\wx0266******1f
  ```

2. Navigate to the root directory of MiniCAT and run `main_reborn.py`:

   ```
   python3 main_reborn.py -h
   ```

   ```
   usage: main_reborn.py [-h] [-i APPID] [-p {wechat,baidu}] [-sp {windows,android}] [-dec {yes,no}]

   optional arguments:
     -h, --help            Show this help message and exit
     -i APPID, --appid APPID
                           The appid of your mini-program.
     -p {wechat,baidu}, --platform {wechat,baidu}
                           The platform you want to analyze.
     -sp {windows,android}, --source {windows,android}
                           Choose the source platform of your mini-app.
     -dec {yes,no}, --justdecrypted {yes,no}
                           Use MiniCAT only for decrypting mini-programs
   ```

   The `-dec` argument is optional.

3. For example, to analyze a mini-program collected from the WeChat PC client, use the following command:

  ```
  python3 main_reborn.py -i wx0266******1f -p wechat -sp windows
  ```

After analyzing, MiniCAT will generate the unpacked source code of the analyzed mini-program in the `dec_dir` directory and a result CSV file in the `res` directory.

4. To analyze multiple mini-programs, use `mutli_query_reborn.py`, which will automatically analyze all mini-programs in the `miniapp_dict` directory.

```
python3 mutli_query_reborn.py
```

## License

The code in this repository is licensed under the [MIT License](https://github.com/github/codeql/blob/main/LICENSE) by [GitHub](https://github.com/).

## Citation

If you create research work that uses our tool, please cite our paper:

```
@inproceedings{MiniCAT:CCS,
  title={MiniCAT: Understanding and Detecting Cross-Page Request Forgery Vulnerabilities in Mini-Programs},
  author={Zidong Zhang and Qingsheng Hou and Lingyun Ying and Wenrui Diao and Yacong Gu and Rui Li and Shanqing Guo and Haixin Duan},
  booktitle={Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security},
  year={2024}
}
```