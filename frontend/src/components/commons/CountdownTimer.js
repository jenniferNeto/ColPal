import React, { useState, useEffect } from "react";

const CountdownTimer = ({ duration }) => {
  const [timeLeft, setTimeLeft] = useState(duration);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setTimeLeft((prevTimeLeft) => Math.max(0, prevTimeLeft - 1000));
    }, 1000);

    return () => clearInterval(intervalId);
  }, [duration]);

  const daysLeft = Math.floor(timeLeft / (1000 * 60 * 60 * 24)).toString().padStart(2, "0");
  const hoursLeft = Math.floor((timeLeft / (1000 * 60 * 60)) % 24).toString().padStart(2, "0");
  const minutesLeft = Math.floor((timeLeft / 1000 / 60) % 60).toString().padStart(2, "0");
  const secondsLeft = Math.floor((timeLeft / 1000) % 60).toString().padStart(2, "0");
  const progress = ((duration - timeLeft) / duration) * 100;
  const circumference = 2 * Math.PI * 50;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className="my-3" style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <svg width="200" height="200" viewBox="0 0 100 100">
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="transparent"
          stroke="#ddd"
          strokeWidth="10"
        ></circle>
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="transparent"
          stroke="#605CA8"
          strokeWidth="10"
          strokeDasharray={`${circumference} ${circumference}`}
          strokeDashoffset={offset}
          transform="rotate(-90, 50, 50)"
          style={{ transition: "stroke-dashoffset 1s linear" }}
        ></circle>
        <text
          x="50"
          y="50"
          textAnchor="middle"
          dominantBaseline="middle"
          fill="#222"
          fontSize="12"
          fontWeight="bold"
        >
          {daysLeft}:{hoursLeft}:{minutesLeft}:{secondsLeft}
        </text>
      </svg>
    </div>
  );
};

export default CountdownTimer;