// generate_dalle_images.js
// Usage:
//   export OPENAI_API_KEY="sk-..."
//   node script/generate_dalle_images.js
// This script calls the OpenAI Image Generation endpoint (DALL·E-like) to create PNG images
// and saves them to assets/images/*.png

import fs from 'fs';
import path from 'path';

const API_KEY = process.env.OPENAI_API_KEY;
if(!API_KEY){
  console.error('Missing OPENAI_API_KEY environment variable.');
  process.exit(1);
}

const outDir = path.resolve('assets/images');
if(!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const prompts = [
  {file: 'ansiedade.png', prompt: 'Abstract, soft-focus illustration representing anxiety and worry, warm muted colors, human silhouette with swirling thoughts, empathetic and non-stigmatizing style'},
  {file: 'depressao.png', prompt: 'Abstract, gentle illustration representing depression, melancholic yet hopeful, cool tones, person sitting with soft light, painterly style'},
  {file: 'toc.png', prompt: 'Stylized illustration representing obsessive-compulsive disorder, repeating patterns and small rituals, calm color palette, conceptual art'},
  {file: 'panico.png', prompt: 'Illustration representing panic attack, sudden burst of energy and breath, clear but sensitive depiction, not graphic, expressive brush strokes'},
  {file: 'esquizofrenia.png', prompt: 'Conceptual illustration representing schizophrenia with auditory hallucinations, abstract sound waves and human profile, respectful and sensitive, muted palette'}
];

async function generate(){
  for(const p of prompts){
    console.log('Generating', p.file);
    try{
      const res = await fetch('https://api.openai.com/v1/images/generations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${API_KEY}` },
        body: JSON.stringify({ prompt: p.prompt, n:1, size: '1024x1024' })
      });
      if(!res.ok){
        const txt = await res.text();
        console.error('OpenAI API error',res.status, txt);
        continue;
      }
      const data = await res.json();
      // expecting b64_json in data.data[0].b64_json
      const b64 = data.data && data.data[0] && (data.data[0].b64_json || data.data[0].b64);
      if(!b64){ console.error('No image data for', p.file); continue }
      const buf = Buffer.from(b64, 'base64');
      fs.writeFileSync(path.join(outDir, p.file), buf);
      console.log('Saved', p.file);
    }catch(err){
      console.error('Error generating',p.file,err);
    }
  }
}

generate();
