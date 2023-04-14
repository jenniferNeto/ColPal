export const parseFrequency = (frequency) => {

    const datetime = frequency.split(' ');
    
    const [hours, minutes, seconds] = datetime[datetime.length-1].split(':');
    const day = datetime.length == 2 ? datetime[0] : '00';

    return [day, hours, minutes, seconds];
}

export const getDuration = (time) => {
    let [day, hours, minutes, seconds] = parseFrequency(time);
  
    day = parseInt(day) * 24 * 60 * 60
    hours =  parseInt(hours) * 60  * 60 
    minutes = parseInt(minutes) * 60
    seconds = parseInt(seconds)

    return day + hours + minutes + seconds;
    
}

export const formatDate = (date) => {
    let parsedDate = new Date( Date.parse(date) );
    return parsedDate.toLocaleString();
}
