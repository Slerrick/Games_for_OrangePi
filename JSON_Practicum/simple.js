document.addEventListener('DOMContentLoaded', () => {
    const scrollContainer = document.querySelector('.image-scroll');
    const firstImageBlock = document.querySelector('.block1');
    const leftArrow = document.querySelector('.left-arrow');
    const rightArrow = document.querySelector('.right-arrow');
    if (!scrollContainer || !firstImageBlock || !leftArrow || !rightArrow) {
        console.error('Не удалось найти необходимые элементы DOM');
        return;
    }
    const getImageBlockWidth = () => {
        return firstImageBlock.clientWidth + 10;
    };
    const scrollToCenter = () => {
        const imageBlockWidth = getImageBlockWidth();
        scrollContainer.scrollTo({
            left: imageBlockWidth * 4,
            behavior: 'smooth'
        });
    };
    const handleLeftArrowClick = () => {
        scrollContainer.scrollBy({
            left: -getImageBlockWidth(),
            behavior: 'smooth'
        });
    };
    const handleRightArrowClick = () => {
        scrollContainer.scrollBy({
            left: getImageBlockWidth(),
            behavior: 'smooth'
        });
    };
    setTimeout(scrollToCenter, 100);
    leftArrow.addEventListener('click', handleLeftArrowClick);
    rightArrow.addEventListener('click', handleRightArrowClick);
});
