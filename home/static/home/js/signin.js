function dostuff(style) {
        style.display = style.display === 'none' ? '' : 'none';
    }
function toggledisplay(elementID1,elementID2)
{
    dostuff(document.getElementById(elementID1).style);
    dostuff(document.getElementById(elementID2).style);
}