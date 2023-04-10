export const parseFrequency = (frequency) => {

    const datetime = frequency.split(' ');
    
    const [hours, minutes, seconds] = datetime[datetime.length-1].split(':');
    const day = datetime.length == 2 ? datetime[0] : '00';

    return [day, hours, minutes, seconds];
}

export const getDuration = (time) => {
    let [day, hours, minutes, seconds] = parseFrequency(time);
  
    day = parseInt(day) * 24 * 60 * 60 *1000,
    hours =  parseInt(hours) * 60  * 60 * 1000,
    minutes = parseInt(minutes) * 60 * 1000,
    seconds = parseInt(seconds) * 1000;

    return day + hours + minutes + seconds;
    
}

export const formatDate = (date) => {
    let parsedDate = new Date( Date.parse(date) );
    return parsedDate.toLocaleString();
}
