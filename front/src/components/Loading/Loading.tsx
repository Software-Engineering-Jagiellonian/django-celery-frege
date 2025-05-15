import React, { useEffect, useState } from 'react';

const Loading = () => {
  const [dots, setDots] = useState(0);

  const printDots = () => {
    let result = 'Loading ';

    for (let i = 0; i < dots; i++) {
      result += '.';
    }

    return result;
  };

  useEffect(() => {
    const playAnimation = setInterval(() => {
      setDots(dots + 1 > 3 ? 0 : dots + 1);
    }, 500);

    return () => clearInterval(playAnimation);
  }, [dots]);

  return <h1>{printDots()}</h1>;
};

export default Loading;
