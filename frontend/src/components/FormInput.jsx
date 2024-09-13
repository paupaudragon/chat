import { useState } from "react";
function FormInput({ setter, ...props }) {

    let onChange;
    if (props.onChange) {
      onChange = props.onChange;
    } else if (setter) {
      onChange = (e) => setter(e.target.value);
    } else {
      onChange = () => {};
    }
    const className = [
      props.className || "",
      "border rounded",
      "px-4 py-2 my-2",
      "border-slate-400",
      "border-2",
      "focus:outline-none",
      "focus: border - orange - 500",
      "focus: outline - white forcus: outline - 0.5",
      // props.readOnly ?
      //   "bg-zinc-700" :
      "bg-transparent border-lgrn",
        
    ].join(" ");
  if (props.readOnly) {
    return (
      <div className="items-center py-2 ">
        <span className="px-4 py-2 my-2 bg-transparent">
          {props.value}
        </span>
      </div>
    );
     
  } else {

    return (
      <div className="flex flex-col py-2">
        <label htmlFor={props.name}>
          {props.name}
          {props.required && <span className="text-pink-500 ml-1">*</span>}
        </label>
        <input
          {...props}
          className={className}
          onChange={onChange}
        />
      </div>
    );
  }

  }
 
  
  export default FormInput;