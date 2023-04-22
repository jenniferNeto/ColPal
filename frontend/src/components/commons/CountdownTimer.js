import React, { useState, useEffect } from "react";

function CountdownTimer({ track, deadline, total }) {
  const [timeLeft, setTimeLeft] = useState(deadline);

  const [progress, setProgress] = useState(100)

  useEffect(() => {
    if(!track) return;
    const interval = setInterval(() => {
      setTimeLeft(Math.max(timeLeft - 1, 0));
      setProgress(Math.floor((timeLeft * 100) / total))
    }, 1000);


    return () => clearInterval(interval);
  }, [timeLeft]);


  const daysLeft = Math.floor(timeLeft / (60 * 60 * 24)).toString().padStart(2, "0");
  const hoursLeft = Math.floor((timeLeft / (60 * 60)) % 24).toString().padStart(2, "0");
  const minutesLeft = Math.floor((timeLeft / 60) % 60).toString().padStart(2, "0");
  const secondsLeft = Math.floor((timeLeft) % 60).toString().padStart(2, "0");

  const circleRadius = 45;
  const circleLength = 2 * Math.PI * circleRadius;

  return (
    <div className="countdown-timer">
      <svg viewBox="0 0 100 100" width="100%" height="100%">
        <circle
          cx="50"
          cy="50"
          r={circleRadius}
          strokeWidth="5"
          stroke="#605CA8"
          fill="transparent"
        />
        <circle
          cx="50"
          cy="50"
          r={circleRadius}
          strokeWidth="5"
          stroke="#eee"
          fill="transparent"
          strokeDasharray={circleLength}
          strokeDashoffset={circleLength - (progress / 100) * circleLength}
          transform="rotate(-90 50 50)"
          style={{ transition: "stroke-dashoffset 1s linear" }}
        />
        <text x="50" y="50" fontSize="10px" textAnchor="middle">
        {daysLeft}:{hoursLeft}:{minutesLeft}:{secondsLeft}
        </text>

      </svg>
    </div>
  );
}

export default CountdownTimer;