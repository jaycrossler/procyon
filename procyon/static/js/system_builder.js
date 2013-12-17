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
    var userVars = 'rand, stellar, temp, mass, radius, age';
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
    document.title="Builder: "+description;

    var data_holder = '<h2>'+settings.name+'</h2><b>'+description+'</b><p>';
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

    $('#data_details')
        .html(data_holder)
        .css({backgroundColor:settings['color']});

    var planet_data = system_builder.buildPlanetDescriptions(settings) || "<b>No planets</b>";

    $('#planet_data')
        .html(planet_data);

    system_builder.buildPlanetCanvas(settings);

};
system_builder.buildPlanetCanvas=function(settings){
    var moon_objects = [];
    _.each(settings.planet_data,function(planet,num){
        var circle_max = 20;
        var radius = parseInt(planet.radius/8*circle_max);

        //Create a stage by getting a reference to the canvas
        var stage = new createjs.Stage('planet_'+num);
        //Create a Shape DisplayObject.
        var circle = new createjs.Shape();
        circle.graphics.beginFill("black").drawCircle(0, 0, radius);
        //Set position of Shape instance.
        circle.x = circle.y = circle_max-3;
        //Add Shape instance to stage display list.
        stage.addChild(circle);
        //Update stage will render next frame

        _.each(planet.moons,function(moon,moon_num){
            var circle = new createjs.Shape();
            var size = 1+parseInt(Math.random()*2);

            var color = createjs.Graphics.getRGB(Math.random()*255|0, Math.random()*255|0, Math.random()*255|0)

            circle.graphics.beginFill(color).drawCircle(0, 0, size);
            circle.x = parseInt(Math.random()*circle_max*2);
            circle.y = parseInt(circle_max-6 + Math.random()*8);
            circle.go_dir = Math.random()<=0.5?'right':'left';
            circle.rot_speed = Math.random();

            stage.addChild(circle);

            moon_objects.push({circle:circle, stage:stage, p_radius:radius});
        });

        stage.update();

    });

    function moveMoons(event) {
        //TODO: Add speed bounce

        _.each(moon_objects,function(obj){
            var circle = obj.circle;
            var stage = obj.stage;
            var planet_left = (stage.canvas.width/2)-obj.p_radius-2;
            var planet_right = (stage.canvas.width/2)+obj.p_radius-2;

            if (circle.go_dir == 'left') {
                circle.x -= circle.rot_speed;
                if (circle.x >= planet_left && circle.x <= planet_right && circle.y >planet_left && circle.y < planet_right-2){
                    circle.alpha=0;
                } else {
                    circle.alpha=1;
                }

            } else {
                circle.x += circle.rot_speed;
            }

            if (circle.x > stage.canvas.width-2) { circle.go_dir='left'; }
            if (circle.x < 2) { circle.go_dir='right'; }

            stage.update(event);
        });

    }



    createjs.Ticker.on("tick", moveMoons);
    createjs.Ticker.setFPS(30);


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
    var types = 'mass:2, radius:1, gravity:1, craterization:1, ring_numbers:0, tilt:0, atmosphere_millibars:thousands, magnetic_field:thousands, num_moons:0';
    var dataVars = 'Mass:mass, Radius:radius, Gravity:gravity, Rings:ring_numbers, Tilt:tilt, Millibars:atmosphere_millibars, Craters:craterization, Mag Field:magnetic_field';

    _.each(settings.planet_data,function(planet,num){
        output += '<span class="planet-info"><h3><canvas id="planet_'+num+'" width="40" height="40"></canvas>'+planet.name+'</h3>';
        var output_list = []

        _.each(dataVars.split(','),function(v){
            v = _.str.trim(v);
            v = v.split(":");
            var title = v[0];
            var field = v[1];

            if (planet[field] !== undefined){
                var val = planet[field];
                val = helpers.typedValues(val,field,types);
                if (val !== undefined) {
                    output_list.push("<span><b>"+title+"</b>: "+ _.str.capitalize(val)+"</span>");
                }
            }
        });
        output+=output_list.join(" : ") + "<br/>";

        if (planet.moons && planet.moons.length){
            output+="<br/>Moons ("+planet.num_moons+"): ";
            _.each(planet.moons,function(moon){
                output+="[<b>"+moon.name+"</b>] ";
            });

        }

        output+="</span>";

    });
    return output;
};