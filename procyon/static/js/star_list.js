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
            return helpers.parsecs_to_ly(data.distance_parsecs);
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
    $.ajax('/maker/star/'+item.id)
        .success(function(data){
            text="";
            if (data.guessed_age && data.guessed_age!="None") text+="<b>Age</b>: "+helpers.round(data.guessed_age)+" Million years old</br>";
            if (data.guessed_mass && data.guessed_mass!="None") text+="<b>Solar Masses</b>: "+helpers.round(data.guessed_mass)+"</br>";
            if (text){
                $('<p>')
                    .html("<b><i>Simulated Data</i></b><br/>"+text)
                    .addClass('small')
                    .appendTo($details);
            }
            $('<p>')
                .html("<b><i>Link To Viewer</i></b>")
                .on('click',function(){
                    document.location.href="/maker/viewer/"+data.id;
                })
                .addClass('small')
                .css({cursor:'pointer',color:'blue'})
                .appendTo($details);

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
        text = helpers.distance_from_parsecs_to_text(item.distance_parsecs,3);
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
            if (planet.radius && planet.radius!="None") text+="Radius: "+helpers.round(planet.radius,1);
            if (planet.mass && planet.mass!="None") text+="Mass: "+helpers.round(planet.mass,2);
            text+="<br/>";
        });
        $('<p>')
            .html("<b><i>Known Planets</i></b><br/>"+text)
            .addClass('small')
            .appendTo($details);
    }

};
