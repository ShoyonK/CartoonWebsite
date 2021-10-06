
const assert = require('assert');
const fs = require('fs');
const path = require("path");

describe('Testing instance.js', function() { 
    before(function (){
        const jsdom = require('jsdom');
        const { JSDOM } = jsdom;
        var htmlString = fs.readFileSync(path.resolve(__dirname, '../../templates/animeinstance.html')).toString();
        this.dom = new JSDOM(htmlString);
    });

    beforeEach(function(){
        const { window } = this.dom;
        const $ = global.jQuery = require('jquery')(window);
        global.$ = $;
        this.instance = require('../../static/js/instance');
    }); 
    
    it('Checks that number of visible cards in carousel is 3', function() {
        assert.equal(this.instance.minPerSlide, 3);
    });  
});