# Omni Pretest
## Summary of Commits
The following commit hashes correspond to the requirements:
- **Order Model**: Commit [0f6e72814aee6584195ebb066e66aef0f7c9b72e](https://github.com/cpching/pretest/commit/0f6e72814aee6584195ebb066e66aef0f7c9b72e)
- **import_order API**: Commit [5ee3117e542530822ad76771577bf3e5ef48cdbe](https://github.com/cpching/pretest/commit/5ee3117e542530822ad76771577bf3e5ef48cdbe)
- **API Unit Test**: Commit [ff8d52731244f5a28dd69e881ea460c95790a7ca](https://github.com/cpching/pretest/commit/ff8d52731244f5a28dd69e881ea460c95790a7ca)
- **Replace Token Check with Decorator**: Commit [46a224faccd74879996eabb11d2d79f1edb390e3](https://github.com/cpching/pretest/commit/46a224faccd74879996eabb11d2d79f1edb390e3)
- **Extend Order Model**: Commit [6d58895ef007f0e52048959d83a323a2b01c2a39](https://github.com/cpching/pretest/commit/6d58895ef007f0e52048959d83a323a2b01c2a39)
- **Creative Extensions**: The rest of the commits


## Setup Environment
* Download [docker](https://www.docker.com/get-started) and Install

* [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this **pretest** project to your own repository

* Clone **pretest** project from your own repository
    ```
    git clone https://github.com/[your own account]/pretest.git
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
* Construct **Order** Model in **api** app (**0f6e72814aee6584195ebb066e66aef0f7c9b72e**)

    The below information is necessary in **Order** model:
    * Order-number
    * Total-price
    * Created-time

* Construct **import_order** api ( POST method ) (**5ee3117e542530822ad76771577bf3e5ef48cdbe**)
    * Validate access token from request data
    
        ( accepted token is defined in **api/views.py** )
    * Parse data and Save to corresponding fields
* Construct api unittest (**ff8d52731244f5a28dd69e881ea460c95790a7ca**)

---
## Advanced Requirements ( optional )
* Replace the statement of checking api access token with a decorator (**46a224faccd74879996eabb11d2d79f1edb390e3**)

* Extend Order model (**6d58895ef007f0e52048959d83a323a2b01c2a39**)
    * Construct **Product** model
    * Build relationships between **Order** and **Product** model

* Get creative and Extend anything you want (The rest of commits)
---
## Submit
* After receiving this pretest, you have to finish it in 7 days
* Create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) and name it with your name ( 王小明 - 面試 )

* Feel free to let us know if there is any question: sophie.lee@bebit-tech.com
