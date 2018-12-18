## Blob
Blob Storage Script to compress and push the compressed files with content encoding gzip

node blobStorage ./assets/<folder> key container

If one needs to push images in `/live/images` on azure, then copy the images in `./assets/images` folder.
If one needs to push images in `/live/images/pwa` on azure, then copy the images in `./assets/images/pwa` folder.

```js
    Example:
    node blobStorage.js ./assets/images <key> live
```
