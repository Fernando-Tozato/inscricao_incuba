function mascara_hora(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "5");
    if (v.length == 2){
        i.value += ":";
    }

    if(v.contains(':')){
        h = v.split(':')[0];
        m = v.split(':')[1];

        if(h<0){
            i.value = '00:00';
        } else if(h==24){
            i.value = '00:00';
        }
    }
}