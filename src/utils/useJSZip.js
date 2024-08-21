import JSZip from 'jszip'
import { saveAs } from 'file-saver'

class ExtendedJSZip extends JSZip {
  downloadAsync(filename, ext = '.zip') {
    if (!filename.endsWith('.zip')) {
      filename = filename + ext
    }

    return this.generateAsync({ type: 'blob' }).then((blob) => {
      saveAs(blob, filename)
    })
  }
}


export default function useJSZip() {
  return new ExtendedJSZip()
}