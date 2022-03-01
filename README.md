# Omni Pretest
## Setup Environment
* Download docker and Installfffff

* Clone **pretest** project 
    ```
    git clone git@github.com:beBit-tech/pretest.git
    ```

* Checkout **pretest** directory
    ```
    cd pretest
    ```

* Start docker container
    ```
    docker-compose up
    ```

* Enter activated **pretest-web-1** container
    ```
    docker exec -it pretest-web-1 bash
    ```
    Note:

    * This container codebase is connected to **pretest** project local codebase
    * If you need to migrate migration files or test testcases, make sure do it in **pretest-web-1** container
---
## Requirements
* Construct **Order** Model in **api** app

    The below information is necessary in **Order** model:
    * Order-number
    * Total-price
    * Created-time

* Construct **import_order** api ( POST method )
    * Check access token is valid 
    
        ( accepted token is defined in **api/views.py** )
    * Parse data and Save to corresponding fields
* Construct api unittest

---
## Advanced Requirements ( optional )
* Replace the statement of checking api access token with a decorator

* Extend Order model
    * Construct Product model
    * Build relationships between Order and Product model

* Get creative and Extend anything you want  
---
## Submit
* After receiving this pretest, you have to finish it in 7 days
* Create a pull request and name it with your name ( 王小明 - 面試 )

* Feel free to let us know if there is any question: shelby.xiao@omniscientai.com
