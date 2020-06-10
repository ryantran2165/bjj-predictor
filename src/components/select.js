import React from "react";
import PropTypes from "prop-types";

const Select = ({ fighters, onChange, id }) => {
  return (
    <select style={{ width: "100%" }} onChange={onChange} id={id}>
      {fighters.map((fighter) => {
        const id = fighter["id"];
        const firstName = fighter["first_name"];
        const nickname = fighter["nickname"];
        const lastName = fighter["last_name"];
        const team = fighter["team"];

        return (
          <option key={id}>
            {firstName}
            {nickname ? ' "' + nickname + '"' : ""}
            {" " + lastName}
            {team ? ", " + team : ""}
          </option>
        );
      })}
    </select>
  );
};

Select.defaultProps = {
  fighters: [],
};

Select.propTypes = {
  fighters: PropTypes.array,
  onChange: PropTypes.func.isRequired,
};

export default Select;
