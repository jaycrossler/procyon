var star_list = {};
star_list.init=function(){

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
        {sTitle: 'Light Years', mData:function(data){
            var parsecs = data.distance_parsecs * 3.26163344;
            return parseInt(parsecs * 100) /100;
        }, sDefaultContent:""}
    ];

    var aSelected = null;
    $table.dataTable( {
        aaData: items,
        bJQueryUI: true,
        sProcessing:true,
        aaSorting: [[7, 'asc']],
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
    var $details = $('#data_details');

    var width = parseInt($details.parent().css('width'))-parseInt($details.parent().children().first().css('width'));
    $details.css({width:width-30}).empty();

    $('<b>')
        .text(item.__unicode__)
        .addClass('center')
        .appendTo($details);

    var text = "";
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
            .html("<b>Identifiers</b>:<br>"+text)
            .addClass('small')
            .appendTo($details);
    }



};