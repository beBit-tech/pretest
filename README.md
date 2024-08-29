# Omni Pretest
## Finished Features

1. Construct **Order** Model in **api** app with the attributes:
    * Order-number
    * Total-price
    * Created-time

2. Construct **import_order** api ( POST method ):
    * Validate access token from request data ( accepted token is defined in **api/AccessValidation.py** )

    * Parse data and Save to corresponding fields

3. Construct **import_order** api unittest

4. Replace the statement of checking api access token with a decorator

5. Extend Order model
    * Construct **Product** model
    * manage relationships between **Order** and **Product** model through **ProductOrder** model

6. order creation
    * update the **import_order** to create ProductOrder to record order informations
    * make the transaction atomic ensure all the database operations are committed,otherwise rollback

7. test feat no.6
    * non-exist product test

8. get order and product information api implementation
    * provide URL endpoints to access product & order detail (GET method)

9. Construct unittest to verify the functionality of features  no.7
    * base functionality test
    * nonexist item test
