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
  {file: 'ansiedade.png', prompt: 'Realistic, empathetic portrait capturing the feeling of anxiety: a person clutching their chest slightly, tense shoulders, shallow breathing; background blurred with subtle swirling shapes to suggest racing thoughts; warm-but-muted tones, soft studio lighting, high-detail, respectful and non-stigmatizing'},
  {file: 'depressao.png', prompt: 'Realistic, gentle scene expressing depression: a person seated by a window with low, soft light, gaze downcast and distant, heavy atmosphere, cool desaturated color palette, subtle grain, emotional but hopeful undertone, respectful portrayal'},
  {file: 'toc.png', prompt: 'Realistic, focused image representing obsessive-compulsive behaviors: close-up of hands arranging small objects precisely in repeated patterns, cool neutral tones, shallow depth of field, crisp detail on hands and objects, conveying tension and the need for order without judgement'},
  {file: 'panico.png', prompt: 'Expressive, respectful depiction of a panic moment: person with widened eyes and slightly open mouth, motion blur around edges to suggest sudden overwhelm, high-contrast lighting with cool highlights, emphasis on immediacy and breathlessness rather than sensationalism'},
  {file: 'esquizofrenia.png', prompt: 'Conceptual but realistic portrait for schizophrenia focusing on experience and feeling: human profile with soft sound-wave and fragmented text overlays suggesting auditory hallucinations, muted color palette, gentle light, avoid caricature—respectful, empathetic and contemplative'}
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
