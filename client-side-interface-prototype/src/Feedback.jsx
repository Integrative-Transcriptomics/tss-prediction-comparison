import React from 'react';

function Feedback({ errorMessage, feedbackMessage }) {
  if (!errorMessage && !feedbackMessage) {
    return null;
  }

  return (
    <div className={`message ${errorMessage ? 'error-message' : 'feedback-message'}`}>
      {errorMessage || feedbackMessage}
    </div>
  );
}

export default Feedback;
