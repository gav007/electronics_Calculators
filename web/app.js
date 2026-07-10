const $ = (id) => document.getElementById(id);
const number = (id) => Number($(id).value);
const show = (id, text) => { $(id).textContent = text; };
const valid = (...values) => values.every((value) => Number.isFinite(value) && value > 0);

function calculate(action) {
  try {
    if (action === 'ohms') {
      const values = [number('voltage'), number('current'), number('resistance')];
      const filled = values.filter((value) => value > 0).length;
      if (filled !== 2) throw new Error('Enter exactly two positive values.');
      let result;
      if (!(values[0] > 0)) result = values[1] * values[2] + ' V';
      else if (!(values[1] > 0)) result = values[0] / values[2] + ' A';
      else result = values[0] / values[1] + ' Ω';
      show('ohms-result', `Result: ${result}`);
    } else if (action === 'power') {
      const v = number('power-v'); const i = number('power-i');
      if (!valid(v, i)) throw new Error('Enter positive voltage and current.');
      show('power-result', `Power: ${(v * i).toFixed(3)} W`);
    } else if (action === 'series' || action === 'parallel') {
      const values = $('resistor-values').value.split(',').map(Number);
      if (!values.length || !valid(...values)) throw new Error('Enter positive comma-separated values.');
      const result = action === 'series' ? values.reduce((a, b) => a + b, 0) : 1 / values.reduce((sum, value) => sum + 1 / value, 0);
      show('resistor-result', `Total: ${result.toFixed(3)} Ω`);
    } else if (action === 'divider') {
      const v = number('divider-v'); const top = number('divider-top'); const bottom = number('divider-bottom');
      if (!valid(v, top, bottom)) throw new Error('Enter positive values.');
      show('divider-result', `Output: ${(v * bottom / (top + bottom)).toFixed(3)} V`);
    } else {
      const resistance = number('rc-r'); const capacitance = number('rc-c');
      if (!valid(resistance, capacitance)) throw new Error('Enter positive values.');
      show('rc-result', `Time constant: ${(resistance * capacitance).toFixed(6)} seconds`);
    }
  } catch (error) {
    show(`${action}-result`, error.message);
  }
}

document.querySelectorAll('button[data-action]').forEach((button) => button.addEventListener('click', () => calculate(button.dataset.action)));
