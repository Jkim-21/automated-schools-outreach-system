const {builder, Builder, By, promise} = require ("selenium-webdriver");

website = "https://www.delasalle.com/"

async function open_and_close(website){
    //open safari
    let driver = await new Builder().forBrowser("safari").build();
    //find websites
    await driver.get(website)
    //close browser
    await driver.close(website)
}

async function fafo(website){

    let driver = await new Builder().forBrowser("safari").build();

    try {
        //open the desired website
        await driver.get(website);

        //elements with tag <a> - filter for more later
            //maybe add parameter for filter later on
        let links = await driver.findElements(By.tagName('a'));

        //collect all href attributes
        let hrefs = await Promise.all(links.map(async link => {
            return await link.getAttribute('href');
        }));
        
        //ignore undefined and null references
        hrefs = hrefs.filter(href => href !== null && href !== undefined);

        //regex for emails and url's - works - should refine later
        let emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
        let urlRegex = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;

        let emails = hrefs.filter(href => emailRegex.test(href));
        let urls = hrefs.filter(href => urlRegex.test(href));

        return { emails, urls };
    } catch (error) {
        console.error("Error:",error);
    } finally {
        await driver.quit();
    }
}

//example websites

let websites = [
    "https://www.delasalle.com/",
    "https://www.colby.edu/",
    "https://central.spps.org/",
    "https://mn01910242.schoolwires.net/Domain/16",
    "https://ehs.district196.org/"
];



(async function() {
    for (let website of websites) {
        let result = await fafo(website);
        console.log(result.emails)
        console.log(result.urls)
    }
})();