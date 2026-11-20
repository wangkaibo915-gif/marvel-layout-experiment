// Galen test suite for the Ironman slide.
// Run from the project root:
//   galen test galen/tests/ironman.test.js --htmlreport reports/galen --parallel-tests 1
// A ChromeDriver must be available on PATH or configured via -Dwebdriver.chrome.driver.

var pageUrl = "http://127.0.0.1:4173/";
var specPath = "galen/specs/ironman.gspec";

test("Ironman slide at 1440x1024", function () {
    var driver = createDriver(pageUrl, "1440x1024", "chrome");
    checkLayout(driver, specPath, ["desktop"]);
    driver.quit();
});
