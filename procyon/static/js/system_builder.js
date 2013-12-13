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
    var spectrum = _.sample('DYTLSCMKGFABMKMKMKGFAB'.split('')) + _.sample('1234567234563455'.split(''));
    if (Math.random()<0.4){
        spectrum += helpers.romanize(_.random(1,6)) + _.sample('ab     '.split(''));
    }
    return spectrum;
};
system_builder.setupStartingVars=function(settings){
    var userVars = 'rand, stellar, temp, mass, radius, age, planets, color';
    var types = 'temp:thousands, mass:3, radius:2, age:thousands';
    var dataVars = 'Type of Star:star_type_name, Luminosity:luminosity_class, Brightness Class:luminosity_mod';

    var qs = {};
    //Set up form variables
    _.each(userVars.split(','),function(v){
        v = _.str.trim(v);
        qs[v] = helpers.queryString(v);
        var val;
        if (settings[v]){
            val = settings[v];
            val = system_builder.typedValues(val,v,types);
        } else {
            val = qs[v] || '';
        }

        $('#'+v).val(val);
    });



    var data_holder = '';
    _.each(dataVars.split(','),function(v){
        v = _.str.trim(v);
        v = v.split(":");
        var title = v[0];
        var val = v[1];

        if (settings[val]){
            val = settings[val];
            val = system_builder.typedValues(val,v,types);
            if (val) {
                data_holder += "<b>"+title+"</b>: "+ _.str.capitalize(val)+"<br/>";
            }

        }
    });
    $('#data_details').html(data_holder);



    $('#color').css({backgroundColor:settings['color']});

//data_holder

};
system_builder.typedValues=function(val,v,types){
    _.each(types.split(','),function(t){
        t = t.split(":");
        var type_name = _.str.trim(t[0]);
        var type_type = t[1];
        if (v == type_name){
            if (helpers.isNumber(type_type)){
                var type_decimals = parseInt(type_type);
                val = helpers.round(val,type_decimals);
                return false;
            } else {
                if (type_type=='thousands'){
                    val = helpers.numberWithCommas(parseInt(val));
                }
            }
        }
    });
    return val;
};