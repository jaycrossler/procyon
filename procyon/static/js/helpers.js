helpers={};
helpers.queryString=function(q) {
    var hu = window.location.search.substring(1);
    var gy = hu.split("&");
    var result = null;
    for (var i=0;i<gy.length;i++) {
        var ft = gy[i].split("=");
        if (ft[0] == q) {
            result = ft[1]; break;
        }
    }
    return result;
};
helpers.lerp = function(in_min, in_max, in_percent) {
    return in_min + in_percent * (in_max - in_min);
};
helpers.mlerp = function(in_min, in_max, in_amount, out_min, out_max) {
    var reverse = (in_min > in_max);
    if (reverse) {
        var in_temp = in_min;
        in_min = in_max;
        in_max = in_temp;
    }
    in_amount = helpers.clamp(in_amount,in_min,in_max);

    var in_percent = (in_amount - in_min) / (in_max - in_min);
    if (reverse) in_percent = 1-in_percent;


    return helpers.lerp(out_min, out_max, in_percent);
};
helpers.clamp = function(value, min, max) {
  return Math.min(Math.max(value, min), max);
};
helpers.round=function(num,digits){
    var pow = Math.pow(10,digits || 2);
    num = parseInt(num * pow) / pow;
    if (num && num > 1000) {
        num = helpers.numberWithCommas(parseInt(num))
    }
    return num;
};
helpers.numberWithCommas=function(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};
helpers.parsecs_to_ly=function(parsecs){
    return helpers.round(parsecs * 3.26163344,2);
};
helpers.distance_from_parsecs_to_text=function(parsecs,numItems){
    var speeds = [];
    numItems = numItems || 3;
    var distances = 'parsecs ly atlas horizons pioneer serenity falcon galactica warp2 warp5 warp99'.split(" ");
    $.each(distances,function(i,distance_name){
        speeds[i] = helpers.parsecs_to(parsecs,distance_name,false);
    });

    var speedlist = _.sample(speeds, numItems);
    return speedlist.join("<br/>\n");

};
helpers.parsecs_to=function(parsecs, distance_name, hideTitle){
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
        var val = result.roundUp? parseInt(parsecs*result.mult) : helpers.round(parsecs * result.mult,1);
        if (val==1 && suffix) suffix=suffix.replace(/s$/,"");

        output = title + val + suffix;
    }
    return output;
};
helpers.isNumber=function(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
};
helpers.romanize=function(num){
    if (!+num)
        return false;
    var digits = String(+num).split(""),
        key = ["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM",
               "","X","XX","XXX","XL","L","LX","LXX","LXXX","XC",
               "","I","II","III","IV","V","VI","VII","VIII","IX"],
        roman = "",
        i = 3;
    while (i--)
        roman = (key[+digits.pop() + (i * 10)] || "") + roman;
    return Array(+digits.join("") + 1).join("M") + roman;
};
helpers.typedValues=function(val,varname,types){
    //Use by passing in an array of types, like:
    //var types = 'temp:thousands, mass:3, radius:2, age:thousands';


    _.each(types.split(','),function(t){
        t = t.split(":");
        var type_name = _.str.trim(t[0]);
        var type_type = t[1];
        if (varname == type_name){
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