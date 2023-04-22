export default function NotificationCard({data}) {
  const {id, message, date, pipeline, user} = data;
  console.log(id, message, date, pipeline, user)

  console.log("Data:", data)
  console.log("Message:", message)
  
  return (
      <div className='card' style={{border: 'none', background: '#E9E7FD', cursor: "pointer"}}>
          <div className='card-body'>
          <div className="card-title d-flex justify-content-between">
            <h5>{message}</h5> 
            <div>
            <span className={`badge me-1 rounded-pill bg-success'}`}>
              {date}</span>
            </div>
          </div>
          </div>
          {/* <div className='card-footer d-flex justify-content-between'>
            <span>Upload Frequency:</span> <span>{`${day}d ${hours}h ${minutes}m  ${seconds}s `}</span>
          </div> */}
      </div>
  
  )
}
