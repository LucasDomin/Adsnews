const API = "http://127.0.0.1:8000/ads";

let ADS = [];

async function loadAds() {
  const res = await fetch(API);
  ADS = await res.json();
  render(ADS);
}

function render(data) {
  const grid = document.getElementById("grid");
  grid.innerHTML = "";

  data.forEach(ad => {
    const div = document.createElement("div");
    div.className = "card";

    div.innerHTML = `
      <h3>${ad.page_name || ""}</h3>
      <p>${ad.headline || ""}</p>
      <small>${ad.media_type || ""}</small>
    `;

    grid.appendChild(div);
  });
}

document.getElementById("search").addEventListener("input", (e) => {
  const q = e.target.value.toLowerCase();

  const filtered = ADS.filter(a =>
    (a.page_name || "").toLowerCase().includes(q) ||
    (a.headline || "").toLowerCase().includes(q)
  );

  render(filtered);
});

loadAds();