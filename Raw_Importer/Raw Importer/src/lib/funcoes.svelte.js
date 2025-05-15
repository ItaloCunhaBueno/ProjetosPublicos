import { Command } from '@tauri-apps/plugin-shell';
import * as path from '@tauri-apps/api/path';
import { convertFileSrc } from '@tauri-apps/api/core';
import { exists, readDir, remove } from '@tauri-apps/plugin-fs';

let rawPermitidos = ['CR3', 'CR2', 'cr3', 'cr2', 'Cr3', 'Cr2'];
let xmpPermitidos = ['XMP', 'Xmp', 'xmp'];

export async function generatePreview(caminho) {
	const filename = await path.basename(caminho, '.CR3');
	const previewName = `${filename}-preview2.jpg`;
	const tempDir = await path.tempDir();
	const command = Command.sidecar('exiv2', ['-q', '-f', '-l', tempDir, '-ep2', caminho], { encoding: 'utf8' });
	const executeCommand = await command.execute();
	const caminhoPreview = await path.join(tempDir, previewName);
	return [filename, caminhoPreview];
}

export async function deletePreviews(listaCaminhos) {
	for (const caminho of listaCaminhos) {
		await remove(caminho);
	}
}

export async function readOrientation(caminho) {
	const rotationValues = {
		0: 0,
		1: 90,
		2: 180,
		3: 270
	};
	const command = Command.sidecar('exiv2', ['-q', '-P', 'v', '-K', 'Exif.CanonSi.AutoRotate', caminho], { encoding: 'utf8' });

	const executeCommand = await command.execute();
	try {
		return rotationValues[parseInt(executeCommand.stdout)];
	} catch (error) {
		console.log(error);
		return undefined;
	}
}

export async function readDate(caminho) {
	const command = Command.sidecar('exiv2', ['-q', '-P', 'v', '-K', 'Exif.Image.DateTime', caminho], { encoding: 'utf8' });

	const executeCommand = await command.execute();
	try {
		let data = executeCommand.stdout.split(' ')[0];
		let hora = executeCommand.stdout.split(' ')[1];
		data = data.replaceAll(':', '-');
		return `${data} ${hora}`;

		// return new Date(dateString);
	} catch (error) {
		console.log(error);
		return undefined;
	}
}

export async function pathVerify(pathString) {
	let valor = await exists(pathString);
	return valor;
}

export async function readFiles(pathString) {
	let files = await readDir(pathString);
	let caminhos = {};

	for (const e of files) {
		let nome = e.name.split('.').at(0);
		let ext = e.name.split('.').at(-1);
		if (rawPermitidos.includes(ext)) {
			let caminho = await path.join(pathString, e.name);
			let dateTime = await readDate(caminho);
			let date = dateTime.split(' ').at(0);
			if (!(date in caminhos)) {
				caminhos[date] = {};
			}
			if (!(nome in caminhos[date])) {
				caminhos[date][nome] = {};
			}
			caminhos[date][nome]['foto'] = await path.join(pathString, e.name);
			let xmp = await path.join(pathString, `${e.name}.xmp`);
			console.log(xmp);
			if (await exists(xmp)) {
				caminhos[date][nome]['xmp'] = xmp;
			}
		}
	}
	return caminhos;
}

export function processaHora(milliseconds) {
	let seconds = Math.floor((milliseconds / 1000) % 60);
	let minutes = Math.floor((milliseconds / (1000 * 60)) % 60);
	let hours = Math.floor((milliseconds / (1000 * 60 * 60)) % 24);

	hours = hours < 10 ? '0' + hours : hours;
	minutes = minutes < 10 ? '0' + minutes : minutes;
	seconds = seconds < 10 ? '0' + seconds : seconds;

	return hours + ':' + minutes + ':' + seconds;
}
