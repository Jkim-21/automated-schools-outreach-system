const {builder, Builder} = require ("selenium-webdriver");

website = "https://www.delasalle.com/"

async function open_new(website){

    //open safari
    let driver = await new Builder().forBrowser("safari").build();

    //find websites
    await driver.get(website)


    //close browser
}


//example websites

/*
https://www.delasalle.com/
https://www.colby.edu/
https://central.spps.org/
https://mn01910242.schoolwires.net/Domain/16
https://ehs.district196.org/
*/

open_new(website)