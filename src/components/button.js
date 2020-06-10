import React from "react";
import PropTypes from "prop-types";

const Button = ({ value, onClick }) => {
  return (
    <input
      className="btn btn-primary btn-lg"
      type="button"
      value={value}
      onClick={onClick}
    />
  );
};

Button.defaultProps = {
  value: "Default value"
};

Button.propTypes = {
  value: PropTypes.string,
  onClick: PropTypes.func.isRequired
};

export default Button;
