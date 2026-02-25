import fs from 'fs';
import path from 'path';
import sharp from 'sharp';

const dir = path.resolve('assets/images');
if(!fs.existsSync(dir)){
  console.error('assets/images not found');
  process.exit(1);
}

const files = fs.readdirSync(dir).filter(f=>f.endsWith('.svg'));
if(files.length===0){ console.error('no svg files found'); process.exit(1); }

async function convert(){
  for(const f of files){
    const inPath = path.join(dir,f);
    const outName = f.replace(/\.svg$/,'') + '.png';
    const outPath = path.join(dir,outName);
    console.log('Converting', f, '->', outName);
    const svg = fs.readFileSync(inPath);
    try{
      await sharp(svg)
        .resize(1024, 768, { fit: 'contain', background: { r:255, g:255, b:255, alpha:1 } })
        .png({ quality: 90 })
        .toFile(outPath);
      console.log('Saved', outPath);
    }catch(err){
      console.error('Error converting', f, err);
    }
  }
}

convert();
