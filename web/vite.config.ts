import { defineConfig } from 'vite';
import {rmSync} from 'node:fs';
export default defineConfig({ base: process.env.BASE_PATH || '/ProjectCobertizo/', build: { chunkSizeWarningLimit: 900 }, server: { port: 5173 }, plugins:[{name:'exclude-pilot-from-production',apply:'build',closeBundle(){rmSync(new URL('./dist/assets/pilot',import.meta.url),{recursive:true,force:true});}}] });
