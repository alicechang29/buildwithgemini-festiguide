// Automated Demo Tour Script for FestiGuide iPhone
window.runDemoTour = async function() {
  console.log("Starting automated demo tour...");

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  // 1. Initial view on Map
  switchScreen('map');
  await sleep(2500);

  // Toggle Satellite View
  const btnSat = document.getElementById('btnSat');
  if (btnSat) {
    btnSat.click();
    await sleep(2000);
  }

  // Toggle back to Streets
  const btnStreet = document.getElementById('btnStreet');
  if (btnStreet) {
    btnStreet.click();
    await sleep(1500);
  }

  // 2. Switch to Timeline Screen
  switchScreen('timeline');
  await sleep(2000);

  // Play audio preview on first act
  const previewBtns = document.querySelectorAll('#timelineList .act-btn');
  if (previewBtns.length > 0) {
    previewBtns[0].click();
    await sleep(4000);
  }

  // Open Swap Modal on first act
  if (previewBtns.length > 1) {
    previewBtns[1].click(); // Swap Act button
    await sleep(2500);
    // Select first alternative
    const swapItems = document.querySelectorAll('.swap-item');
    if (swapItems.length > 0) {
      swapItems[0].click();
      await sleep(2500);
    }
  }

  // 3. Switch to Discovery Screen
  switchScreen('discovery');
  await sleep(2500);

  // 4. Switch to Profile Screen
  switchScreen('profile');
  await sleep(2500);

  // 5. Open Dream Poster
  showPoster();
  await sleep(3000);
  hidePoster();
  await sleep(1000);

  // 6. Return to Map
  switchScreen('map');
  console.log("Demo tour complete!");
};
