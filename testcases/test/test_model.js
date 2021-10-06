
const assert = require('assert');
const fs = require('fs');
const path = require("path");

describe('Testing model.js', function() { 
    before(function (){
        const jsdom = require('jsdom');
        const { JSDOM } = jsdom;
        var htmlString = fs.readFileSync(path.resolve(__dirname, '../../templates/animemodel.html')).toString();
        this.dom = new JSDOM(htmlString);
    });

    beforeEach(function(){
        const { window } = this.dom;
        const $ = global.jQuery = require('jquery')(window);
        global.$ = $;
        this.model = require('../../static/js/model');
    }); 
    
    it('Check that page size is 9 instances', function() {
        assert.equal($('.pagination').data("page-size"), 9);
    });

    it('Check that number of pages for anime/character models is 12', function (){
        var result = this.model.computeNumPages(100);
        assert.equal(result, 12);
    });

    it('Check that number of pages for studio/staff models is 5', function (){
        var result = this.model.computeNumPages(40);
        assert.equal(result, 5);
    });

    it('Checks that the correct number of pagination buttons were generated', function(){
        var nPages = 12;
        this.model.generateButtons(nPages);
        assert.equal($(".page-link").length, nPages+2); //+2 because of prev and next buttons
    });

    it('Checks that the num-page data attribute was stored correctly', function(){
        var nPages = 12;
        this.model.saveNumPages(nPages);
        assert.equal($(".pagination").data("num-pages"), 12);
    });


    // Some debugging/logging functions
    // See entire html after javascript acts on it
    // console.log($('html').html()); //jQuery style
    // console.log(dom.window.document.querySelector("html").innerHTML); //JavaScript style

    // select a data attribute in javascript
    // console.log(dom.window.document.querySelector(".pagination").dataset.pageSize);
    // Set a data attribute in jQuery
    // $(".pagination").data("num-pages", 12)
  
});