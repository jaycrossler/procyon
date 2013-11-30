var star_list = {};
star_list.star_types=[];
star_list.init=function(){
    $.ajax('/stars/starmodels/').success(function(data){
        star_list.star_types = data;
    })
};
star_list.buildTable=function(items){
    var $table = $('#data_holder');

    var columnInfo = [
        {sTitle: 'ID', mData:'id', sDefaultContent:""},
        {sTitle: 'Name', mData:'__unicode__', sDefaultContent:"", mRender:function(data,type,full){
            var out = data;
            if (full.web_color){
                out = "<span style='background-color:"+full.web_color+"'>"+out+"</span>";
            }
            return out;
        }},
        {sTitle: 'Spectrum', mData:'spectrum', sDefaultContent:""},
        {sTitle: 'LY', mData:function(data){
            return star_list.parsecs_to_ly(data.distance_parsecs);
        }, sDefaultContent:""}
        ,{sTitle: 'Planets', mData:'known_planet_count', sDefaultContent:""}
    ];

    var aSelected = null;
    $table.dataTable( {
        aaData: items,
        bJQueryUI: true,
        sProcessing:true,
        aaSorting: [[7, 'asc']],
        bScrollCollapse: true,
        bScrollInfinite: true,
        sScrollY:250,
        sDom: 't<"clear">',
        aoColumns:columnInfo,
        fnRowCallback: function (nRow){
            if (aSelected != nRow.DT_RowId){
                $(nRow).removeClass('row_selected');
            }
        }
    });

    $table.find('tbody tr').live('click',function(){
        var row = this;
        aSelected = row.id;

        $table.find('tbody tr').removeClass('row_selected');
        $(row).addClass('row_selected');

        var aData = $table.fnGetData( this );
        star_list.showDetails(aData);

    }).css({cursor:'pointer'});
};
star_list.showDetails=function(item){
    var $details = $('#data_details')
        .css({backgroundColor:item.web_color});

    var text = "";
    $.ajax('/maker/star/prime/'+item.id)
        .success(function(data){
            text=""
            if (data.guessed_age) text+="<b>Age</b>: "+star_list.round(data.guessed_age)+" Million years old</br>";
            if (data.guessed_mass) text+="<b>Solar Masses</b>: "+star_list.round(data.guessed_mass)+"</br>";
            if (text){
                $('<p>')
                    .html("<b><i>Simulated Data</i></b><br/>"+text)
                    .addClass('small')
                    .appendTo($details);
            }
        });

    var width = parseInt($details.parent().css('width'))-parseInt($details.parent().children().first().css('width'));
    $details.css({width:width-34}).empty();

    $('<b>')
        .text(item.__unicode__)
        .addClass('center')
        .appendTo($details);

    if (item.HIP && item.HIP!="None") {
        text+="Hipparcos ID: <a href='http://www.rssd.esa.int/hipparcos_scripts/HIPcatalogueSearch.pl?hipId="+item.HIP+"' target='_blank'>"+item.HIP+"</a><br/>";
    }
    if (item.HD && item.HD!="None") {
        text+="Draper ID: <a href='http://www.rssd.esa.int/hipparcos_scripts/HIPcatalogueSearch.pl?hdId="+item.HD+"' target='_blank'>"+item.HD+"</a><br/>";
    }
    if (item.HR && item.HR!="None") {
        text+="Hoffleit Bright Star ID: <a href='http://www.stellar-database.com/Scripts/search_star.exe?Catalog=HR&CatNo="+item.HR+"' target='_blank'>"+item.HR+"</a><br/>";
    }
    if (item.gliese && item.gliese!="None") {
        var gl = item.gliese;
        if (gl.length){
            gl = gl.match(/(\d+)$/);
            if (gl && gl.length){
                gl = parseInt(gl[0], 10);
                text+="Gliese ID: <a href='http://www.stellar-database.com/Scripts/search_star.exe?Catalog=Gl&CatNo="+gl+"' target='_blank'>"+gl+"</a><br/>";
            }
        }
    }
    if (item.bayer_flamsteed && item.bayer_flamsteed!="None") text+="Yale Bright Star ID: "+item.bayer_flamsteed+"<br/>";

    if (text){
        $('<p>')
            .html("<b><i>Identifiers</i></b>:<br>"+text)
            .addClass('small')
            .appendTo($details);
    }

    if (item.distance_parsecs){
        text = star_list.distance_from_parsecs_to_text(item.distance_parsecs,3);
        $('<p>')
            .html("<b><i>Distance</i></b>:<br>"+text)
            .addClass('small')
            .appendTo($details);
    }


    if (item.possibly_habitable){
        $('<p>')
            .html("<b>Likely Planet in Habitable Zone</b>")
            .addClass('small')
            .appendTo($details);
    }

    if (item.known_planets && item.known_planets.length){
        text = "";
        _.each(item.known_planets,function(planet){
            text+="<b>"+planet.name+"</b>: ";
//            if (planet.other_name) text+="("+planet.other_name+") ";
            if (planet.radius && planet.radius!="None") text+="Radius: "+star_list.round(planet.radius,1);
            if (planet.mass && planet.mass!="None") text+="Mass: "+star_list.round(planet.mass,2);
            text+="<br/>";
        });
        $('<p>')
            .html("<b><i>Known Planets</i></b><br/>"+text)
            .addClass('small')
            .appendTo($details);
    }

};
star_list.round=function(num,digits){
    var pow = Math.pow(10,digits || 2);
    var num = parseInt(num * pow) / pow;
    if (num && num > 1000) {
        num = star_list.numberWithCommas(parseInt(num))
    }
    return num;
};
star_list.parsecs_to_ly=function(parsecs){
    return star_list.round(parsecs * 3.26163344,2);
};
star_list.distance_from_parsecs_to_text=function(parsecs,numItems){
    var speeds = [];
    numItems = numItems || 3;
    var distances = 'parsecs ly atlas horizons pioneer serenity falcon galactica warp2 warp5 warp99'.split(" ");
    $.each(distances,function(i,distance_name){
        speeds[i] = star_list.parsecs_to(parsecs,distance_name);
    });

    var speedlist = _.sample(speeds, numItems);
    return speedlist.join("<br/>\n");

};
star_list.parsecs_to=function(parsecs, distance_name, hideTitle){
    //parsec = 3.08567758 × 10^13 km / year
    // 36000 km/h = 315567360 km/yr
    // 3.08567758 x 10^13 / (36000 * 24 * 365.24)
    // 1 AU = 149,597,870.7 km
    // 1 LY = 9.4605284 × 10^12 km
    // 16 d / 1 AU =  9349866.91875 km / day

    var distance_db = [
        {name:'parsecs',title:"Parsecs", mult:1, suffix:""},
        {name:'ly',title:"Light Speed", mult:3.26163344, suffix:"years"},
        {name:'atlas',title:"Atlas V Rocket", mult:97781.899, suffix:"years"}, //3.08567758 x 10^13 / (36000 * 24 * 365.24)
        {name:'horizons',title:"New Horizons", mult:61113.687, suffix:"years"},
        {name:'pioneer',title:"Pioneer 10", mult:63540.584, suffix:"years"},
        {name:'serenity',title:"Serenity", mult:9035.8, suffix:"years"}, // 16 d / 1 AU =  9349866.91875 km / day
        {name:'falcon',title:"Millenium Falcon", mult:0.5436, suffix:"hours"}, //(3.08567758 × 10^13) / ((4.2 * 9.4605284 X 10^12) / (42/60) * 365.24)
        {name:'galactica',title:"Battlestar Gallactica", mult:0.2042066, suffix:"jumps", roundUp:true}, //3.08567758 × 10^13 / (4600 * (9.4605284 × 10^12) * 365.24) * 365.24 * 24 * 12
        {name:'warp2',title:"Enterprise Warp 2", mult:119.127899803, suffix:"days"},
        {name:'warp5',title:"Enterprise Warp 5", mult:5.56672428986, suffix:"days"}, // (3.08567758 × 10^13) / (214 * 9.4605284 × 10^12) * 365.24
        {name:'warp99',title:"Enterprise Warp 9.9", mult:0.39019947528, suffix:"days"} // (3.08567758 × 10^13) / (3053 * 9.4605284 × 10^12) * 365.24
    ];
    var result = _.find(distance_db,function(item){return item.name==distance_name});
    var output = "";
    if (result){
        var title = hideTitle?"":("<b>"+result.title+"</b>: ");
        var suffix = result.suffix?(" "+result.suffix):"";
        var val = result.roundUp? parseInt(parsecs*result.mult) : star_list.round(parsecs * result.mult,1);
        if (val==1 && suffix) suffix=suffix.replace(/s$/,"");

        output = title + val + suffix;
    }
    return output;
};
star_list.numberWithCommas=function(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}