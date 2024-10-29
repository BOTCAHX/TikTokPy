/**
 * The code below is a jQuery script that handles form interaction and AJAX
 * for downloading content from TikTok. This script uses SweetAlert2
 * to display notifications to the user during the data fetching process
 * and after the data has been successfully retrieved.
 
 @ Made by BOTCAHX 
 */
 
 
$(document).ready(function() {
    $('#downloadForm').on('submit', function(event) {
        event.preventDefault();
        const url = $('#url').val();

        Swal.fire({
            title: 'Loading...',
            text: 'Please wait while we get the content details.',
            didOpen: () => {
                Swal.showLoading();
            },
            background: 'rgba(255, 255, 255, 0.8)',
            backdrop: 'rgba(0, 0, 0, 0.4)',
            customClass: {
                title: 'text-purple-600',
                content: 'text-gray-700'
            }
        });

        $.ajax({
            url: '/download',
            type: 'GET',
            data: { url: url },
            success: function(data) {
                Swal.close();
                if (data.video && data.audio && data.title) {
                    let contentHtml = '';
                    let isVideo = data.video.length === 1;
                    let isPhotoCollection = data.video.length > 1;

                    if (isVideo) {
                        contentHtml = `
                            <video controls class="w-full mb-4 rounded-lg shadow-lg max-w-full h-auto">
                                <source src="${data.video[0]}" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        `;
                    } else if (isPhotoCollection) {
                        contentHtml = `
                            <div class="swiper-container">
                                <div class="swiper-wrapper">
                                    ${data.video.map(photo => `
                                        <div class="swiper-slide">
                                            <img src="${photo}" alt="Photo" class="w-full h-full object-cover rounded-lg">
                                        </div>
                                    `).join('')}
                                </div>
                                <div class="swiper-pagination"></div>
                                <div class="swiper-button-next"></div>
                                <div class="swiper-button-prev"></div>
                            </div>
                        `;
                    } else {
                        contentHtml = `<img src="${data.video[0]}" alt="Photo" class="mb-4 mx-auto rounded-lg shadow-lg max-w-full h-auto">`;
                    }

                    Swal.fire({
                        title: `<span class="text-sm font-semibold text-purple-600">${data.title}</span>`,
                        html: `
                            ${contentHtml}
                            <div class="flex flex-wrap justify-center gap-4 mt-4">
                                ${isVideo ? `
                                    <button id="videoDownload" class="bg-yellow-500 text-white py-2 px-6 rounded-full hover:bg-yellow-600 transition duration-300 flex items-center hover-lift">
                                        <span class="material-icons">videocam</span>
                                        Download Video
                                    </button>
                                ` : isPhotoCollection ? `
                                    <button id="bulkDownload" class="bg-green-500 text-white py-2 px-6 rounded-full hover:bg-green-600 transition duration-300 flex items-center hover-lift">
                                        <span class="material-icons">file_download</span>
                                        Download All Photos
                                    </button>
                                ` : `
                                    <button id="photoDownload" class="bg-yellow-500 text-white py-2 px-6 rounded-full hover:bg-yellow-600 transition duration-300 flex items-center hover-lift">
                                        <span class="material-icons">image</span>
                                        Download Photo
                                    </button>
                                `}
                                <button id="audioDownload" class="bg-purple-500 text-white py-2 px-6 rounded-full hover:bg-purple-600 transition duration-300 flex items-center hover-lift">
                                    <span class="material-icons">audiotrack</span>
                                    Download Audio
                                </button>
                            </div>
                        `,
                        showCloseButton: true,
                        background: 'rgba(255, 255, 255, 0.9)',
                        backdrop: 'rgba(0, 0, 0, 0.4)',
                        customClass: {
                            container: 'rounded-lg',
                            popup: 'rounded-lg',
                        },
                        didOpen: () => {
                            if (isPhotoCollection) {
                                new Swiper('.swiper-container', {
                                    slidesPerView: 1,
                                    spaceBetween: 30,
                                    loop: true,
                                    pagination: {
                                        el: '.swiper-pagination',
                                        clickable: true,
                                    },
                                    navigation: {
                                        nextEl: '.swiper-button-next',
                                        prevEl: '.swiper-button-prev',
                                    },
                                });
                            }
                        }
                    });

                    if (isVideo) {
                        $('#videoDownload').on('click', function() {
                            window.location.href = data.video[0];
                        });
                    } else if (isPhotoCollection) {
                        $('#bulkDownload').on('click', function() {
                            data.video.forEach((photo, index) => {
                                window.open(photo, '_blank');
                            });
                        });
                    } else {
                        $('#photoDownload').on('click', function() {
                            window.location.href = data.video[0];
                        });
                    }

                    $('#audioDownload').on('click', function() {
                        window.location.href = data.audio[0];
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Invalid response data.',
                        background: 'rgba(255, 255, 255, 0.9)',
                        backdrop: 'rgba(0, 0, 0, 0.4)'
                    });
                }
            },
            error: function(error) {
                Swal.close();
                console.error('Error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong!',
                    background: 'rgba(255, 255, 255, 0.9)',
                    backdrop: 'rgba(0, 0, 0, 0.4)'
                });
            }
        });
    });
});