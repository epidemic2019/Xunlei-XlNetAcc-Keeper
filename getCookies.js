var cookies = document.cookie.split('; ').reduce((prev, current) => {
    const [name, value] = current.split('=');
    prev[name] = value;
    return prev
  }, {});
console.log(btoa(JSON.stringify(cookies)));