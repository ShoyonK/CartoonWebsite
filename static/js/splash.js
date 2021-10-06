// Images asset
const animeImages = {
    1:'static/images/SNKSelectFrames/scene00145.jpg',
    2:'static/images/SNKSelectFrames/scene00147.jpg',
    3:'static/images/SNKSelectFrames/scene00149.jpg',
    4:'static/images/SNKSelectFrames/scene00151.jpg',
    5:'static/images/SNKSelectFrames/scene00153.jpg',
    6:'static/images/SNKSelectFrames/scene00155.jpg',
    7:'static/images/SNKSelectFrames/scene00157.jpg',
    8:'static/images/SNKSelectFrames/scene00159.jpg',
    9:'static/images/SNKSelectFrames/scene00161.jpg',
    10:'static/images/SNKSelectFrames/scene00163.jpg',
    11:'static/images/SNKSelectFrames/scene00165.jpg',
    12:'static/images/SNKSelectFrames/scene00167.jpg',
    13:'static/images/SNKSelectFrames/scene00169.jpg',
    14:'static/images/SNKSelectFrames/scene00171.jpg',
    15:'static/images/SNKSelectFrames/scene00173.jpg',
    16:'static/images/SNKSelectFrames/scene00175.jpg',
    17:'static/images/SNKSelectFrames/scene00177.jpg',
    18:'static/images/SNKSelectFrames/scene00179.jpg',
    19:'static/images/SNKSelectFrames/scene00181.jpg',
    20:'static/images/SNKSelectFrames/scene00183.jpg',
    21:'static/images/SNKSelectFrames/scene00185.jpg',
    22:'static/images/SNKSelectFrames/scene00187.jpg',
    23:'static/images/SNKSelectFrames/scene00189.jpg',
    24:'static/images/SNKSelectFrames/scene00191.jpg',
    25:'static/images/SNKSelectFrames/scene00193.jpg',
    26:'static/images/SNKSelectFrames/scene00195.jpg',
    27:'static/images/SNKSelectFrames/scene00197.jpg',
    28:'static/images/SNKSelectFrames/scene00199.jpg',
    29:'static/images/SNKSelectFrames/scene00201.jpg',
    30:'static/images/SNKSelectFrames/scene00203.jpg',
    31:'static/images/SNKSelectFrames/scene00205.jpg',
    32:'static/images/SNKSelectFrames/scene00207.jpg',
    //33:'static/SNKSelectFrames/scene00209.jpg',
    //34:'static/SNKSelectFrames/scene00211.jpg',
}

const textStyle = {
    1: {opacity: 0, transform: '0px'},
    2: {opacity: 0, transform: '0px'},
    3: {opacity: 0, transform: '0px'},
    4: {opacity: 0, transform: '0px'},
    5: {opacity: .25, transform: '15px'},
    6: {opacity: .5, transform: '10px'},
    7: {opacity: .75, transform: '5px'},
    8: {opacity: 1, transform: '0px'},
    9: {opacity: 1, transform: '0px'},
    10: {opacity: 1, transform: '0px'},
    11: {opacity: 1, transform: '0px'},
    12: {opacity: 1, transform: '0px'},
    13: {opacity: 1, transform: '0px'},
    14: {opacity: 1, transform: '0px'},
    15: {opacity: 1, transform: '0px'},
    16: {opacity: 1, transform: '0px'},
    17: {opacity: 1, transform: '0px'},
    18: {opacity: 1, transform: '0px'},
    19: {opacity: 1, transform: '0px'},
    20: {opacity: 1, transform: '0px'},
    21: {opacity: .75, transform: '15px'},
    22: {opacity: .5, transform: '10px'},
    23: {opacity: .25, transform: '5px'},
    24: {opacity: 0, transform: '0px'},
    25: {opacity: 0, transform: '0px'},
    26: {opacity: 0, transform: '0px'},
    27: {opacity: 0, transform: '0px'},
    28: {opacity: 0, transform: '0px'},
    29: {opacity: 0, transform: '0px'},
    30: {opacity: 0, transform: '0px'},
    31: {opacity: 0, transform: '0px'},
    32: {opacity: 0, transform: '0px'},
    //33: {opacity: 0, transform: '0px'},
    //34: {opacity: 0, transform: '0px'},
}

const step = 30; // For each 30px, change an image

function trackScrollPosition() {
    const y = window.scrollY;
    const label = Math.min(Math.floor(y/30) + 1, 34);
    const imageToUse = animeImages[label];

    //Background i
    $('.image-container').css('background-image', `url('${imageToUse}')`);

    //Text
    const textStep = 2;
    const textStyleToUseLine1 = textStyle[Math.max(20, label)];
    const textStyleToUseLine2 = textStyle[Math.min(Math.max(label - textStep, 1), 32)];
    const textStyleToUseLine3 = textStyle[Math.min(Math.max(label - textStep * 2, 1),32)];
    const textStyleToUseLine4 = textStyle[Math.min(Math.max(label - textStep * 3, 1),32)];
    $('#line1').css({'opacity': textStyleToUseLine1.opacity, 'transform': `translateY(${textStyleToUseLine1.transform})`});
    $('#line2').css({'opacity': textStyleToUseLine2.opacity, 'transform': `translateY(${textStyleToUseLine2.transform})`});
    $('#line3').css({'opacity': textStyleToUseLine3.opacity, 'transform': `translateY(${textStyleToUseLine3.transform})`});
    $('#line4').css({'opacity': textStyleToUseLine4.opacity, 'transform': `translateY(${textStyleToUseLine4.transform})`});

}

$(document).ready(()=>{
    $(window).scroll(()=>{
        trackScrollPosition();
    })
})