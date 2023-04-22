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
      <div className='card' style={{border: 'none', background: '#E9E7FD', cursor: "pointer"}}>
          <div className='card-body'>
          <div className="card-title d-flex justify-content-between">
            <h5>{pipeline_title}</h5> 
            <div>
            <span className={`badge rounded-pill bg-${danger ? 'danger': 'success'}`}>
              {title}</span>
            </div>
          </div>
          <p>{message}</p>
          </div>
          <div className='card-footer d-flex justify-content-between'>
            <span>Sent:</span> <span>{formatDate(date)}</span>
          </div>
      </div>
  
  )
}
