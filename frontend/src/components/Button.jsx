function Button(props) {
    const className = [
      props.className || "",
      "border rounded",
      "px-4 py-2 my-4",
      "border-slate-400",
      "border-2",
      props.disabled ?
      "bg-slate-400 italic" :
      "border-lgrn bg-transparent hover:bg-gray-500",
    ].join(" ");
  
    return (
      <button {...props} className={className}>
        {props.children}
      </button>
    );
  }
  
  export default Button;