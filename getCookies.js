var cookies = document.cookie.split('; ').reduce((prev, current) => {
    const [name, value] = current.split('=');
    prev[name] = value;
    return prev
  }, {});
cookies["kn-speed-peer-id"] = localStorage["kn-speed-peer-id"];
console.log(btoa(JSON.stringify(cookies)));