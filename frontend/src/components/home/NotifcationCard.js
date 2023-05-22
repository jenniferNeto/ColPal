function formatDate(dateString) {
  const date = new Date(dateString);
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const year = date.getFullYear();

  const hourString = hours % 12 === 0 ? "12" : hours % 12;
  const amPm = hours < 12 ? "AM" : "PM";
  const minuteString = minutes < 10 ? `0${minutes}` : minutes;

  const formattedDate = `${hourString}:${minuteString} ${amPm} ${month}/${day}/${year}`;

  return formattedDate;
}

export default function NotificationCard({data}) {
  const {id, message, date, pipeline, pipeline_title, user, title} = data;
  const danger = title === "Position Removed" || title === "Request Rejected" || title === "Pipeline Unstable"  
  return (
    
      <div className='py-4 px-3 bg-main-100 rounded-xl cursor-pointer'>
          <div className="flex justify-between mb-3">
            <span className="font-bold">{pipeline_title}</span> 
            

            <span className='inline-block rounded-full px-2 py-1 mx-1 text-sm font-semibold text-white' style={{background: !danger ? '#50C878': 'red'}}>
                {title}
            </span>
           
          </div>

          <p>{message}</p>

          <hr className='my-2' />

          <div className='flex justify-between'>
            <span>Sent:</span> <span>{formatDate(date)}</span>
          </div>

      </div>
  
  )
}
