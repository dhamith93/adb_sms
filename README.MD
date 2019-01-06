# ADB_SMS
GUI tool to send sms via ADB.

Tested on android `7.x` & `8.x`. Should work with android `5.x+`

## Usage
run `main.py`

* Manual
    * Enter receiver number and message then clicking send button.
* Server
    * Enter port and a key, click start button
    * Send a post request to the `http://<server>:<port>` with:
        * `rec => <reciver_number_w_country_code>`
        * `msg => <msg_body>`
        * `key => <key>`

## Rquirements
* USB debugging enabled android device
* ADB tools

