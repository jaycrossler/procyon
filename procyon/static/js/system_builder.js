var system_builder = {};

system_builder.init= function(settings){
    settings = settings || {};

    system_builder.setupStartingVars(settings);

    $('#randomize').on('click',function(e){
        var stellarClass = system_builder.randomStellarClass();
        window.location.href = "./builder?stellar="+stellarClass;
    });

};
system_builder.randomStellarClass=function(){
    var spectrum = _.sample('DYTLSCMKGOFABMKMKMMKGFAB'.split('')) + _.sample('123456789234563455              '.split(''));
    if (Math.random()<0.4){
        spectrum += helpers.romanize(_.random(1,6)) + _.sample('ab     '.split(''));
    }
    spectrum = spectrum.replace(" ","");
    return spectrum;
};
system_builder.setupStartingVars=function(settings){
    var userVars = 'rand, stellar, temp, mass, radius, age, planets, color';
    var types = 'temp:thousands, mass:3, radius:2, age:thousands';
//    var dataVars = 'Type:star_type_name, Luminosity:luminosity_class, Brightness Class:luminosity_mod';
    var dataVars = 'Brightness Class:luminosity_mod';

    var qs = {};
    //Set up form variables
    _.each(userVars.split(','),function(v){
        v = _.str.trim(v);
        qs[v] = helpers.queryString(v);
        var val;
        if (settings[v] !== undefined){
            val = settings[v];
            val = helpers.typedValues(val,v,types);
        } else {
            val = qs[v] || '';
        }

        $('#'+v).val(val);
    });


    //Set up additional data
    var description = system_builder.buildStarDescription(settings);
    document.title=description;

    var data_holder = '<b>'+description+'</b><p>';
    _.each(dataVars.split(','),function(v){
        v = _.str.trim(v);
        v = v.split(":");
        var title = v[0];
        var val = v[1];

        if (settings[val]){
            val = settings[val];
            val = helpers.typedValues(val,v,types);
            if (val) {
                data_holder += "<b>"+title+"</b>: "+ _.str.capitalize(val)+"<br/>";
            }

        }
    });

    var n_match  = ntc.name(settings.color);
    var colorName = n_match[1];
    data_holder += "<b>Color</b>: "+ _.str.capitalize(colorName)+"<br/><hr/>";


    data_holder += system_builder.buildPlanetDescriptions(settings);
    $('#data_details').html(data_holder);


    $('#color').css({backgroundColor:settings['color']});

};
system_builder.buildStarDescription=function(settings){

    var size = '';
    var dense = '';
    var temp ='';
    var age='';
    if (settings.radius < 0.8) {
        size = 'small';
        if (settings.radius < 0.4) {
            size = 'tiny';
        } else if (settings.radius < 0.2) {
            size = 'mini';
        } else if (settings.radius < 0.1) {
            size = 'miniscule';
        }
        if (settings.mass > 2) {
            dense = 'dense'
        } else if (settings.mass > 4) {
            dense = 'very dense'
        }
        if (settings.mass < .5) {
            dense = 'thin'
        } else if (settings.mass < .2) {
            dense = 'very thin'
        }
    } else if (settings.radius > 3) {
        size = 'big';
        if (settings.radius > 5) {
            size = 'large';
        } else if (settings.radius > 8) {
            size = 'huge';
        } else if (settings.radius > 15) {
            size = 'giant';
        }
        if (settings.mass > 5) {
            dense = 'dense'
        } else if (settings.mass > 8) {
            dense = 'very dense'
        }
        if (settings.mass < 1) {
            dense = 'thin'
        } else if (settings.mass < .5) {
            dense = 'very thin'
        }
    }

    if (settings.temp < 3000) {
        temp = 'cool';
    } else if (settings.temp < 1000) {
        temp = 'cold';
    } else if (settings.temp < 700) {
        temp = 'frigid';
    } else if (settings.temp > 7000) {
        temp = 'warm';
    } else if (settings.temp > 10000) {
        temp = 'hot';
    } else if (settings.temp > 14000) {
        temp = 'burning';
    }

    if (settings.age < 3000) {
        age = 'young';
    } else if (settings.age < 800) {
        age = 'baby';
    } else if (settings.age < 200) {
        age = 'new';
    } else if (settings.age > 8000) {
        age = 'old';
    } else if (settings.age > 12000) {
        age = 'ancient';
    }

    var description = age+' '+size+' '+temp+' '+dense+' '+settings.luminosity_class+' '+settings.star_type_name;
    description = _.str.trim(description);
    description = description.toLowerCase();
    description = _.str.capitalize(description);

    return description;

};
system_builder.buildPlanetDescriptions=function(settings){
    var output='';
    _.each(settings.planet_data,function(planet){
        output += '<b>Planet: '+planet.name+'</b><br/>';
    });
    return output;
};