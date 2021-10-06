function computeNumRows(){
    return $('.container .card').length;
}

function computeNumPages(nRows) {
    return Math.ceil(nRows / $('.pagination').data('page-size'));
}

function generateButtons(nPages){
    for(var i=1; i<nPages; i++) {
        $('<li/>').append($('<a/>', {class: "page-link", href: "#", text: i + 1})).insertBefore('.pagination li:has([rel]):last');
    }
}

function saveNumPages(nPages){
    $('.pagination').data('num-pages', nPages);
}

function doPagination() {
    //var nRows = (typeof nRows !== 'undefined') ?  nRows : $('.container .card').length;
    
    //calculate the number of pages in pagination
    var nRows = computeNumRows();
    var nPages = computeNumPages(nRows);

    // save num pages as a data attribute of pagination element
    saveNumPages(nPages);

    // Dynamically generate buttons
    generateButtons(nPages);

    //do pagination
    $('.pagination li').on('click', function (e) {
        // prevent default action
        e.preventDefault();

        // The clicked element is the next one......
        var eleClicked = $(this);
        var nextEle = eleClicked;

        // ....if the clicked element is Next or Prev buttons
        var nextPrevAnchorEle = eleClicked.find('a[rel]');
        if (nextPrevAnchorEle.length == 1) {
            // compute the next element
            if (nextPrevAnchorEle.text().trim() == 'Next') {
                nextEle = $('.pagination li.active').next('li:not(:has([rel]))');
                if (nextEle.length == 0) {
                    nextEle = $('.pagination li:not(:has([rel])):first');
                }
            } else {
                nextEle = $('.pagination li.active').prev('li:not(:has([rel]))');
                if (nextEle.length == 0) {
                    nextEle = $('.pagination li:not(:has([rel])):last');
                }
            }
        }

        // toggle active page
        $('.pagination li.page-item.active').removeClass('active');
        nextEle.addClass('page-item active');

        // get the number of active page
        var currentPageNumber = +nextEle.find('a').text().trim() - 1;

        // get the page size
        var pageSize = +$('.pagination').data('page-size');
        
        // toggle visibility
        $('.container .card:visible').toggle(false);
        $('.container .card').slice(currentPageNumber * pageSize, (currentPageNumber + 1) * pageSize).toggle(true);
    });

    // show the active page
    $('.pagination li.active a').trigger('click');
}

$(doPagination());

$(document).on('click', '.allow-focus', function (e) {
    e.stopPropagation();
  });
    
module.exports = {
    doPagination: doPagination,
    computeNumRows: computeNumRows,
    computeNumPages: computeNumPages,
    generateButtons: generateButtons,
    saveNumPages: saveNumPages
}
